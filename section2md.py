import re
import bs4

def normalize_whitespace(text):
    """
    Standardize whitespace in text by replacing multiple spaces with a single space
    and trimming leading/trailing whitespace.
    """
    return re.sub(r'\s{2,}', ' ', text)


def getContentBefore(para, name):
        content_before = ""
        for child in para.children:
            if isinstance(child, bs4.Tag) and child.name == name:
                break
            child_content = normalize_whitespace(child.get_text(separator=" ", strip=True)).strip()
            if child_content: 
                content_before += child_content + " "
        return content_before.strip()

def parseInnerParagraph(para):
    paragraph_text = ""
    content_before = getContentBefore(para, "paragraph")
    for para in para.find_all("paragraph"):
        if para.find("subparagraph"):
            paragraph_text += f"\t{getContentBefore(para, "subparagraph")}\n"
            for subpara in para.find_all("subparagraph"):
                subpara_text = f"\t\t{normalize_whitespace(subpara.get_text(separator=' ', strip=True))}\n"
                paragraph_text += subpara_text
            continue

        paragraph_text += f"\t{normalize_whitespace(para.get_text(separator=' ', strip=True))}\n"

    return content_before, paragraph_text


def section2md(section):
    text = ""
    heading_no = None
    tags = list(section)

    for note in section.find_all("sourceNote"):
        note.decompose()

    for i, tag in enumerate(tags):
        # print(tag)
        if isinstance(tag, bs4.NavigableString):
            text += normalize_whitespace(tag.strip())
        elif tag.name == "heading":
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
                content_before, paragraph_text = parseInnerParagraph(tag)

                if content_before:
                    text += f"### {content_before}\n{paragraph_text}\n"
                else:
                    text += f"{paragraph_text}\n"
                continue

            text += f"### {normalize_whitespace(tag.get_text(separator=' ', strip=True))}\n\n"

        elif tag.name == "paragraph":
            if tag.find("subparagraph"):
                text += f"\t{getContentBefore(tag, "subparagraph")}\n"
                for subpara in tag.find_all("subparagraph"):
                    subpara_text = f"\t\t{normalize_whitespace(subpara.get_text(separator=' ', strip=True))}\n"
                    text += subpara_text
                continue
            text += f"\t{normalize_whitespace(tag.get_text(separator=' ', strip=True))}\n"

        else:
            if tag.find("paragraph"):
                content_before, paragraph_text = parseInnerParagraph(tag)
                text += f"{content_before}\n{paragraph_text}\n"
                continue
            text += f"{normalize_whitespace(tag.get_text(separator=' ', strip=True))}\n"
    
    return text.strip()
            


text = """<schedule id="ID_1438402599206_001" name="sch0" reason="inEffect" startPeriod="2020-06-18" status="operational" temporalId="sch0">
   <num value="0">
    Schedule
   </num>
   <note class="align_right" role="crossReferences" type="inline">
    [
    <ref href="/hk/cap112V/s2">
     s.
                2
    </ref>
    ]
    <marker role="blank-line"/>
    <marker role="blank-line"/>
   </note>
   <heading>
    Article
            9 of the Agreement between the Government of the Hong Kong Special Administrative Region
            of the People’s Republic of China and the Government of the State of Israel Concerning
            Air Services
    <marker role="blank-line"/>
    <marker role="blank-line"/>
   </heading>
   Done, in
        duplicate, at Hong Kong on the 19th day of March 1998 in the English and Hebrew
            languages.
   <crossHeading>
   </crossHeading>
   <text class="align_center">
    “
    <b>
     ARTICLE
                9
    </b>
    <marker role="blank-line"/>
    <marker role="blank-line"/>
    <b>
     Avoidance of Double
                Taxation
    </b>
    <marker role="blank-line"/>
    <marker role="blank-line"/>
   </text>
   <subsection class="left_indent_18 first_line_indent_0" id="ID_1586835421656_001" name="1" temporalId="sch0_1">
    <num class="align_left" value="1">
     (1)
    </num>
    <content>
     Income or profits derived from the operation of aircraft in international
                traffic by an airline of one Contracting Party, including participation in a pool
                service, a joint air transport operation or an international operating agency, which
                are subject to tax in the area of that Contracting Party shall be exempt from income
                tax, profits tax and all other taxes on income or profits imposed in the area of the
                other Contracting Party.
    </content>
   </subsection>
   <subsection class="left_indent_18 first_line_indent_0" id="ID_1586835421656_002" name="2" temporalId="sch0_2">
    <num class="align_left" value="2">
     (2)
    </num>
    <content>
     Capital and assets of an airline of one Contracting Party relating to the
                operation of aircraft in international traffic shall be exempt from taxes of every
                kind and description on capital and assets imposed in the area of the other
                Contracting Party.
     <marker role="section-break"/>
    </content>
   </subsection>
   <subsection class="left_indent_18 first_line_indent_0" id="ID_1586835421656_003" name="3" temporalId="sch0_3">
    <num class="align_left" value="3">
     (3)
    </num>
    <content>
     Gains from the alienation of aircraft operated in international traffic and
                movable property pertaining to the operation of such aircraft which are received by
                an airline of one Contracting Party shall be exempt from any tax on gains imposed in
                the area of the other Contracting Party.
    </content>
   </subsection>
   <subsection class="left_indent_18 first_line_indent_0" id="ID_1586835421656_004" name="4" temporalId="sch0_4">
    <num class="align_left" value="4">
     (4)
    </num>
    <leadIn>
     For the purposes of this Article:
    </leadIn>
   </subsection>
   <subsection id="ID_1586835421656_005" name="0" temporalId="sch0_0">
    <paragraph id="ID_1586835421656_006" name="a" temporalId="sch0_0_a">
     <num value="a">
      (a)
     </num>
     <def name="IncomeOrProfits">
      <content>
       the term “
       <term class="old_format">
        income or profits
       </term>
       ” includes
                        revenues and gross receipts from the operation of aircraft for the carriage
                        of persons, livestock, goods, mail or merchandise in international traffic
                        including:
      </content>
     </def>
     <subparagraph id="ID_1586835421656_007" name="i" role="subSubParagraph" temporalId="sch0_0_a_i">
      <num value="i">
       (i)
      </num>
      <content>
       the charter or rental of aircraft;
      </content>
     </subparagraph>
     <subparagraph id="ID_1586835421656_008" name="ii" role="subSubParagraph" temporalId="sch0_0_a_ii">
      <num value="ii">
       (ii)
      </num>
      <content>
       the sale of tickets or similar documents, and the provision of services
                        connected with such carriage, either for the airline itself or for any other
                        airline; and
      </content>
     </subparagraph>
     <subparagraph id="ID_1586835421656_009" name="iii" role="subSubParagraph" temporalId="sch0_0_a_iii">
      <num value="iii">
       (iii)
      </num>
      <content>
       interest on funds directly connected with the operation of aircraft in
                        international traffic;
      </content>
     </subparagraph>
    </paragraph>
    <paragraph id="ID_1586835421656_010" name="b" temporalId="sch0_0_b">
     <num value="b">
      (b)
     </num>
     <def name="InternationalTraffic">
      the term “
      <term class="old_format">
       international
                        traffic
      </term>
      ” means any carriage by an aircraft except when such carriage
                    is solely between places in the area of the other Contracting Party;
     </def>
    </paragraph>
    <paragraph id="ID_1586835421656_011" name="c" temporalId="sch0_0_c">
     <num value="c">
      (c)
     </num>
     <def name="AirlineOfOneContractingParty">
      the term “
      <term class="old_format">
       airline
                        of one Contracting Party
      </term>
      ” means, in the case of the Hong Kong Special
                    Administrative Region, an airline incorporated and having its principal place of
                    business in the Hong Kong Special Administrative Region and, in the case of the
                    State of Israel, an airline substantially owned and effectively controlled by
                    the Government of the State of Israel or its
                    nationals;
      <marker role="section-break"/>
     </def>
    </paragraph>
    <paragraph id="ID_1586835421656_012" name="d" temporalId="sch0_0_d">
     <num value="d">
      (d)
     </num>
     <def name="CompetentAuthority">
      the term “
      <term class="old_format">
       competent
                        authority
      </term>
      ” means, in the case of the Hong Kong Special Administrative
                    Region, the Commissioner of Inland Revenue or his authorised representative, or
                    any person or body authorised to perform any functions at present exercisable by
                    the Commissioner or similar functions, and, in the case of the State of Israel,
                    the State Revenue Administration, Ministry of Finance, or their authorised
                    representative.
     </def>
    </paragraph>
   </subsection>
   <subsection class="left_indent_18 first_line_indent_0" id="ID_1586835421656_013" name="5" temporalId="sch0_5">
    <num class="align_left" value="5">
     (5)
    </num>
    <content>
     The competent authorities of the Contracting Parties shall, through
                consultation, endeavour to resolve by mutual agreement any disputes regarding the
                interpretation or application of this Article. Article 18 (Settlement of Disputes)
                shall not apply to any such dispute.
    </content>
   </subsection>
   <subsection class="left_indent_18 first_line_indent_0" id="ID_1586835421656_014" name="6" temporalId="sch0_6">
    <num class="align_left" value="6">
     (6)
    </num>
    <leadIn>
     Notwithstanding Article 22 (Entry into Force) each Contracting Party shall
                notify to the other the completion of the procedures required by its law for the
                bringing into force of this Article and the Article shall thereupon have
                effect:
    </leadIn>
   </subsection>
   <subsection id="ID_1586835421671_015" name="0" temporalId="sch0_0">
    <paragraph id="ID_1586835421671_016" name="a" temporalId="sch0_0_a">
     <num value="a">
      (a)
     </num>
     <content>
      in the Hong Kong Special Administrative Region, for any year of assessment
                    beginning on or after 1st April in the calendar year next following that in
                    which this Agreement enters into force;
     </content>
    </paragraph>
    <paragraph id="ID_1586835421671_017" name="b" temporalId="sch0_0_b">
     <num value="b">
      (b)
     </num>
     <content>
      in the State of Israel, for any year of assessment beginning on or after
                    1st January in the calendar year next following that in which this Agreement
                    enters into force.
     </content>
    </paragraph>
   </subsection>
   <subsection class="left_indent_18 first_line_indent_0" id="ID_1586835421671_018" name="7" temporalId="sch0_7">
    <num class="align_left" value="7">
     (7)
    </num>
    <leadIn>
     Notwithstanding Article 20 (Termination) where notice of termination of this
                Agreement is given under that Article, this Article shall cease to have
                effect:
     <marker role="section-break"/>
    </leadIn>
   </subsection>
   <subsection id="ID_1586835421671_019" name="0" temporalId="sch0_0">
    <paragraph id="ID_1586835421671_020" name="a" temporalId="sch0_0_a">
     <num value="a">
      (a)
     </num>
     <content>
      in the Hong Kong Special Administrative Region, for any year of assessment
                    beginning on or after 1st April in the calendar year next following that in
                    which notice is given;
     </content>
    </paragraph>
    <paragraph id="ID_1586835421671_021" name="b" temporalId="sch0_0_b">
     <num value="b">
      (b)
     </num>
     <content>
      in the State of Israel, for any year of assessment beginning on or after
                    1st January in the calendar year next following that in which notice is
                    given.
     </content>
    </paragraph>
   </subsection>
   <subsection class="left_indent_18 first_line_indent_0" id="ID_1586835421671_022" name="8" temporalId="sch0_8">
    <num class="align_left" value="8">
     (8)
    </num>
    <content>
     This Article shall cease to have effect in the event that an agreement for the
                avoidance of double taxation with respect to taxes on income, providing for similar
                exemptions to those in this Article, enters into force between the Contracting
                Parties.”.
    </content>
   </subsection>
  </schedule>"""

if __name__ == "__main__":
    soup = bs4.BeautifulSoup(text, "xml")
    print(section2md(soup.find("schedule")))
