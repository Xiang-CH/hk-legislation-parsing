import os
import re
import bs4
import json
import tiktoken
from tqdm import tqdm
from markdownify import markdownify as md
from section2md import section2md, normalize_whitespace
from inference import getReference


# Debug flag to control verbose output
DEBUG = True
# Flag to control whether to overwrite existing parsed files
OVERWRITE = False
# Flag to control whether to parse references
LLM_PARSE_REFERENCES = True
# Output directory for parsed legislation data
BASE_PATH = "parsed_data"
# Directory containing raw legislation XML files
RAW_DATA_PATH = "raw_legislation"
TOKEN_ENCODER = "o200k_base"

interp_translation = {
    "en": "Interpretation",
    "tc": "釋義",
    "sc": "释义"
}

# Create output directory if it doesn't exist
if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)


def processSections(sec, cap_obj):
    # Process each section
    # Skip sections that are too short, have no ID, or are not in effect, or have no heading (replealed)    
    sec_name = sec.get("temporalId")
    sec_no = sec.get("name")[1:]
    xpid = sec.get("id")
    heading = normalize_whitespace(sec.find("heading").get_text(separator=" ", strip=True).strip()) if sec.find("heading") else None

    # Remove source notes
    for note in sec.find_all("sourceNote"):
        note.decompose()

    # Extract interpretation definitions
    if len(sec.find_all("def")) > 0:
        for interp in sec.find_all("def"):
            if interp.find("term") is None:
                continue
            references = []
            term_def = normalize_whitespace(interp.text.strip())
            if LLM_PARSE_REFERENCES and len(ref_tags) > 0:
                try:
                    references = getReference(cap_obj["cap_no"], sec_no, None, term_def)
                except: 
                    pass
            cap_obj["interpretations"].append({
                "term": normalize_whitespace(interp.find("term").text),
                "text": term_def,
                "ref_tags": [normalize_whitespace(str(ref)) for ref in interp.find_all("ref")],
                "references": references
            })
        
    # Convert tables to markdown format
    for table in sec.find_all("table"):
        new_table = soup.new_tag("content")
        new_table.string = "\n\n" + md(table.prettify()).strip() + "\n\n"
        table.replace_with(new_table)

    # Extract section text and find interpretation terms used
    ref_tags = [normalize_whitespace(str(ref)) for ref in sec.find_all("ref")]

    # section_text = normalize_whitespace(sec.get_text(separator=" ").strip())
    section_text, subsections = section2md(sec, cap_obj["cap_no"],sec_no, LLM_PARSE_REFERENCES)
    interp_terms = [interp["term"] for interp in cap_obj["interpretations"] if interp["term"].lower() in section_text.lower()]

    section_token_count = len(tiktoken.get_encoding(TOKEN_ENCODER).encode(section_text))
    identifier = cap_obj["identifier"]
    url = cap_obj["url"]

    references = []
    if len(subsections) > 0:
        references = [r for s in subsections for r in s["references"]]
    elif interp_translation[cap_obj["language"]] in heading:
        pass
    elif LLM_PARSE_REFERENCES and len(ref_tags) > 0:
        try:
            references = getReference(cap_obj["cap_no"], sec_no, None, section_text)
        except: 
            pass
    
    return {
        "no": sec_no,
        "name": sec_name,
        "heading": heading,
        "text": section_text,
        "subsections": subsections,
        "token_count": section_token_count,
        "url": url.replace("full", sec_name),
        "eleg_url": "https://www.elegislation.gov.hk" + identifier + "?xpid=" + xpid if xpid else None,
        "interp_terms": interp_terms,
        "ref_tags": ref_tags,
        "references": references
    }

# Process files for each language (English, Traditional Chinese, Simplified Chinese)
# for lang in ['en', 'tc', 'sc']:
for lang in ['en']:
    # Get all non-hidden files in the language directory
    files_names = [f for f in os.listdir(f"{RAW_DATA_PATH}/{lang}") if not f.startswith(".")]

    total_token_lang = 0
    processed = 0

    # Process each legislation file with progress bar
    for file_name in tqdm(sorted(files_names), desc=f"Parsing ({lang})"):
        processed += 1

        # Extract chapter number from filename
        cap = file_name.split("_")[1]  # cap number

        # Skip if already processed
        if not OVERWRITE and lang in os.listdir(BASE_PATH) and f"cap_{cap}_{lang}.json" in os.listdir(f"{BASE_PATH}/{lang}"):
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
                "total_token_count": 0,
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
                section_tag = soup.new_tag("section", attrs={"name": "s0", "temporalId": "shortTitle"})
                num_tag = soup.new_tag("num", attrs={"value": "0"})
                section_tag.append(num_tag)
                section_tag.append(content_tag)
                sections = [section_tag]

            total_token_count = 0

            # Process each section
            for sec in sections:
                if len(sec.text) < 5 or sec.get("temporalId") is None or (sec.get("reason") and sec.get("reason") != "inEffect") or sec.get("temporalId").startswith("sch"):
                    continue 
                sec_data = processSections(sec, cap_obj)
                total_token_count += sec_data["token_count"]
                cap_obj["sections"].append(sec_data)

            # Process each schedule
            for sch in schedules:
                if len(sec.text) < 5 or sch.get("temporalId") is None or (sch.get("reason") and sch.get("reason") != "inEffect"):
                    continue
                sch_text = section2md(sch, cap_obj["cap_no"], sch.get("name"), LLM_PARSE_REFERENCES)[0]
                token_count = len(tiktoken.get_encoding(TOKEN_ENCODER).encode(sch_text))
                total_token_count += token_count
                sch_data = {
                    "no": sch.get("name")[3:],
                    "name": sch.get("name"),
                    "heading": normalize_whitespace(sch.find("heading").get_text(separator=" ", strip=True).strip()) if sch.find("heading") else None,
                    "text": sch_text,
                    "url": url.replace("full", sch.get("name")),
                    "eleg_url": "https://www.elegislation.gov.hk" + identifier + "?xpid=" + sch.get("id") if sch.get("id") else None,
                    "token_count": token_count,
                    "sections": []
                }
                if sch.find("section"):
                    for sch_sec in sch.find_all("section"):
                        if len(sch_sec.text) < 5 or not sch_sec.get("temporalId"):
                            continue
                        sch_data["sections"].append(processSections(sch_sec, cap_obj))
                cap_obj["schedules"].append(sch_data)

            cap_obj["total_token_count"] = total_token_count
            total_token_lang += total_token_count

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
        
        # for debugging
        # if processed == 4:
        #     print(f"cap. {cap}")
        #     exit()
    
    print(f"Total token count for {lang}: {total_token_lang}")
