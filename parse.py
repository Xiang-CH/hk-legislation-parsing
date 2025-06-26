import bs4
from tqdm import tqdm
import json
import os
import re
from markdownify import markdownify as md

# Debug flag to control verbose output
DEBUG = True
# Output directory for parsed legislation data
BASE_PATH = "parsed_data"
# Directory containing raw legislation XML files
RAW_DATA_PATH = "raw_legislation"

def normalize_whitespace(text):
    """
    Standardize whitespace in text by replacing multiple spaces with a single space
    and trimming leading/trailing whitespace.
    """
    return re.sub(r'\s{2,}', ' ', text).strip()

# Create output directory if it doesn't exist
if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)

# Process files for each language (English, Traditional Chinese, Simplified Chinese)
# for lang in ['en', 'tc', 'sc']:
for lang in ['en']:
    # Get all non-hidden files in the language directory
    files_names = [f for f in os.listdir(f"{RAW_DATA_PATH}/{lang}") if not f.startswith(".")]

    # Process each legislation file with progress bar
    for file_name in tqdm(sorted(files_names), desc=f"Parsing ({lang})"):
        # Extract chapter number from filename
        cap = file_name.split("_")[1]  # cap number

        # Skip if already processed
        if lang in os.listdir(BASE_PATH) and f"cap_{cap}_{lang}.json" in os.listdir(f"{BASE_PATH}/{lang}"):
            continue

        # Load the XML file
        file = f"{RAW_DATA_PATH}/{lang}/{file_name}/" + [f for f in os.listdir(f"{RAW_DATA_PATH}/{lang}/{file_name}") if f.endswith(".xml")][0]
        with open(file, "r") as f:
            soup = bs4.BeautifulSoup(f.read(), "xml")

        # Parse metadata
        meta = soup.find("meta")
        status = meta.find("docStatus").text  # status of the legislation
        if status != "In effect":  # skip if repealed
            continue
        doc_date = meta.find("dc:date").text  
        identifier = meta.find("dc:identifier").text.split("!")[0] 

        # Determine legislation type (regulation or ordinance)
        cap_type = "reg" if bool(re.search(r'[A-Za-z]', cap)) else "ord"

        # if DEBUG: 
        #     print("========CAP: {}========".format(cap))
        
        # Construct URL for the legislation
        url = f'https://hklii.hk/{lang}/legis/{cap_type}/{str(cap)}/full'
        try:
            # Initialize legislation object
            cap_obj = {
                "cap_no": cap,
                "cap_type": cap_type,
                "identifier": identifier,
                "language": lang,
                "interpretations": [],
                "title": normalize_whitespace(soup.find("docTitle").text).strip() if cap_type=="reg" else normalize_whitespace(soup.find("shortTitle").text).strip() if soup.find("shortTitle") else None,
                "long_title": normalize_whitespace(soup.find("longTitle").text).strip() if cap_type=="ord" else None,
                "url": url,
                "eleg_url": "https://www.elegislation.gov.hk" + identifier,
                "date": doc_date,
                "sections": [],
                "schedules": []
            }
            
            # Find all sections and schedules
            sections = soup.find_all("section")
            schedules = soup.find_all("schedule")

            # Handle case where no sections are found
            if len(sections) == 0:
                # Find paragraphs that aren't part of schedules
                paragraphs = [p for p in soup.find_all(["paragraph", "text"]) if not p.get("temporalId") or not p.get("temporalId").startswith("sch")]
                
                # Create a synthetic section containing all paragraph content
                content_tag = soup.new_tag("content")
                content_tag.string = " ".join([normalize_whitespace(p.get_text(separator=" ").strip()) for p in paragraphs]) 
                section_tag = soup.new_tag("section", attrs={"name": "full", "temporalId": "id"})
                num_tag = soup.new_tag("num", attrs={"value": "0"})
                section_tag.append(num_tag)
                section_tag.append(content_tag)
                sections = [section_tag]


            for type in ["sections", "schedules"]:

                if type == "sections":
                    items = sections
                else:
                    items = schedules

                # Process each section
                for sec in items:
                    # Skip sections that are too short, have no ID, or are not in effect, or have no heading (replealed)
                    if len(sec.text) < 5 or sec.get("temporalId") is None or (sec.get("reason") and sec.get("reason") != "inEffect") or not sec.find("heading"):
                        continue 

                    # Extract section number
                    # try:
                    #     sec_no = sec.find("num").get("value")
                    #     sec.find("num").replace_with("")  # Remove number tag after extraction
                    # except:
                    #     continue

                    sec_name = sec.get("name")
                    xpid = sec.get("id")
                    heading = normalize_whitespace(sec.find("heading").text)
                        
                    # Convert tables to markdown format
                    for table in sec.find_all("table"):
                        new_table = soup.new_tag("content")
                        new_table.string = "\n\n" + md(table.prettify()).strip() + "\n\n"
                        table.replace_with(new_table)

                    # Remove source notes
                    for note in sec.find_all("sourceNote"):
                        note.decompose()

                    # Extract section text and find interpretation terms used
                    references = [ref.prettify() for ref in sec.find_all("ref")]
                    section_text = normalize_whitespace(sec.get_text(separator=" ").strip())
                    interp_terms = [interp["term"] for interp in cap_obj["interpretations"] if interp["term"].lower() in section_text.lower()]
                    
                    # Add section to legislation object
                    cap_obj[type].append({
                        # "no": sec_no,
                        "name": sec_name,
                        "heading": heading,
                        "text": section_text,
                        "url": url.replace("full", sec_name),
                        "eleg_url": "https://www.elegislation.gov.hk" + identifier + "?xpid=" + xpid,
                        "interp_terms": interp_terms,
                        "ref_tags": references,
                        "references": []
                    })

                    # Extract interpretation definitions
                    if len(sec.find_all("def")) > 0:
                        for interp in sec.find_all("def"):
                            if interp.find("term") is None:
                                continue
                            cap_obj["interpretations"].append({
                                "term": normalize_whitespace(interp.find("term").text),
                                "text": normalize_whitespace(interp.text.strip())
                            })

            # Create language directory if it doesn't exist
            if not os.path.exists(f"{BASE_PATH}/{lang}"):
                os.mkdir(f"{BASE_PATH}/{lang}")

            # Save parsed legislation as JSON
            with open(f"{BASE_PATH}/{lang}/cap_{cap}_{lang}.json", "w") as f:
                f.write(json.dumps(cap_obj, ensure_ascii=False, indent=2))
            
        except Exception as e:
            # Handle and report errors
            print(f"Error in cap {cap}: {e}")
            print("File:", file)
            with open(f"cap_{cap}_{lang}.xml", "w") as f:
                f.write(soup.prettify())
            
            raise e
    
