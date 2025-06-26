import re
import bs4

def normalize_whitespace(text):
    """
    Standardize whitespace in text by replacing multiple spaces with a single space
    and trimming leading/trailing whitespace.
    """
    return re.sub(r'\s{2,}', ' ', text)

def section2md(section):
    text = ""
    heading_no = None
    tags = list(section)

    for note in section.find_all("sourceNote"):
        note.decompose()

    for i, tag in enumerate(tags):
        if tag.name == "heading":
            if heading_no:
                text += f"## {heading_no} {normalize_whitespace(tag.get_text(separator=" ", strip=True))}\n\n"
                heading_no = None
            else:
                text += f"## {normalize_whitespace(tag.get_text(separator=" ", strip=True))}\n\n"

        elif tag.name == "num":
            if i + 1 < len(tags) and tags[i + 1].name == "heading":
                heading_no = tag.text
            else:
                text += f"{tag.text} "

        elif tag.name in ["sourceNote"]:
            continue

        elif tag.name == "subsection":
            if tag.find("paragraph"):
                # Append text from all elements preceding the first paragraph
                content_before = ""
                for child in tag.children:
                    if isinstance(child, bs4.Tag) and child.name == "paragraph":
                        break
                    child_content = normalize_whitespace(child.get_text(separator=" ", strip=True)).strip()
                    if child_content: 
                        content_before += child_content + " "

                text += f"### {content_before}\n"

                for para in tag.find_all("paragraph"):
                    text += f"\t{normalize_whitespace(para.get_text(separator=' ', strip=True))}\n"

                text += "\n"
                continue

            text += f"### {normalize_whitespace(tag.get_text(separator=' ', strip=True))}\n\n"
        else:
            text += f"{normalize_whitespace(tag.get_text(separator=' ', strip=True))}\n"
    
    return text.strip()
            


text = """<section id="ID_1438402520145_001" name="s13" reason="inEffect" startPeriod="2020-11-29" status="operational" temporalId="s13"><num value="13">13.</num><heading>Citation of Ordinance</heading><subsection id="ID_1438410782962_004" name="1" temporalId="s13_1"><num value="1">(1)</num><leadIn>Where any Ordinance is referred to, it shall be sufficient for all purposes to
                cite such Ordinance by—</leadIn><paragraph id="ID_1438410782962_012" name="a" temporalId="s13_1_a"><num value="a">(a)</num><content>the title, short title or citation thereof;</content></paragraph><paragraph id="ID_1438410782962_020" name="b" temporalId="s13_1_b"><num value="b">(b)</num><content>its number among the Ordinances of the year in which it was enacted;
                    or</content></paragraph><paragraph id="ID_1438410782977_005" name="c" temporalId="s13_1_c"><num value="c">(c)</num><leadIn>any chapter number lawfully given to it under the authority of—</leadIn><subparagraph id="ID_1483429737793_001" name="1" temporalId="s13_1_c_1"><num value="1">(i)</num><content>the Legislation Publication Ordinance
                        (Cap.
                        614);
                        or</content></subparagraph><subparagraph id="ID_1483429737808_002" name="2" temporalId="s13_1_c_2"><num value="2">(ii)</num><content>any other Ordinance providing for the issue of a revised or other
                        edition of the laws of Hong Kong. <sourceNote>(Replaced <ref href="hk/2011/13">13 of 2011 s. 29</ref>)</sourceNote></content></subparagraph></paragraph></subsection><subsection id="ID_1438410782977_012" name="2" temporalId="s13_2"><num value="2">(2)</num><leadIn>Any reference made to any Ordinance, in accordance with the provisions of
                subsection (1), may be made according to the title, short title, citation, number or
                chapter number used
                in—
                    <sourceNote>(Amended <ref href="hk/2020/21">21 of 2020 s. 7</ref>)</sourceNote></leadIn><paragraph id="ID_1604369753523_001" name="a" temporalId="s13_2_a"><num value="a">(a)</num><content>copies of Ordinances printed by the Government Printer; or</content></paragraph><paragraph id="ID_1604369753523_002" name="b" temporalId="s13_2_b"><num value="b">(b)</num><content>verified copies of Ordinances. <sourceNote>(Amended <ref href="hk/2020/21">21 of 2020 s. 7</ref>)</sourceNote></content></paragraph></subsection><subsection id="ID_1604369753523_003" name="3" temporalId="s13_3"><num value="3">(3)</num><leadIn>In this section— </leadIn><def name="VerifiedCopies"><term>verified copies</term> (<term xml:lang="zh-Hant-HK">經核證文本</term>) means
                verified copies within the meaning of <ref>section 5(1)</ref> of the Legislation
                Publication Ordinance (<ref href="/hk/cap614">Cap. 614</ref>). <sourceNote>(Added <ref href="hk/2020/21">21 of 2020 s. 7</ref>)</sourceNote></def></subsection><sourceNote>(Amended <ref href="/hk/1974/ln57">L.N. 57 of 1974</ref>)</sourceNote></section>"""

soup = bs4.BeautifulSoup(text, "xml")
print(section2md(soup.find("section")))
