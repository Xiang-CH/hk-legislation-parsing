from openai import OpenAI

MODEL = "deepseek-r1-distill-qwen-32b"
client = OpenAI(
    base_url="http://localhost:5000/v1",
    api_key="EMPTY"
)


def chatCompletion(messages, functions=None, kwargs=None):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        functions=functions,
        **kwargs
    )
    reasoning_content = response.choices[0].message.reasoning_content
    content = response.choices[0].message.content

    return reasoning_content, content


def chatCompletionStream(messages, functions=None, kwargs={}):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        functions=functions,
        stream=True,
        **kwargs
    )
    for chunk in response:
        yield chunk.choices[0].delta.content

text = "12A. Admiralty jurisdiction of Court of First Instance (1) The Admiralty jurisdiction of the Court of First Instance shall consist of— (a) jurisdiction to hear and determine any of the questions and claims mentioned in subsection (2); (b) jurisdiction in relation to any of the proceedings mentioned in subsection (3); (c) any other Admiralty jurisdiction which it had immediately before the commencement of the Supreme Court (Amendment) Ordinance 1989 ( 3 of 1989 ). (2) The questions and claims referred to in subsection (1)(a) are— (a) any claim to the possession or ownership of a ship or to the ownership of any share therein; (b) any question arising between the co-owners of a ship as to possession, employment or earnings of that ship; (c) any claim in respect of a mortgage of or charge on a ship or any share therein; (d) any claim for damage received by a ship; (e) any claim for damage done by a ship; (f) any claim for loss of life or personal injury sustained in consequence of any defect in a ship or in her apparel or equipment, or in consequence of the wrongful act, neglect or default of— (i) the owners, charterers or persons in possession or control of a ship; or (ii) the master or crew of a ship, or any other person for whose wrongful acts, neglects or defaults the owners, charterers or persons in possession or control of a ship are responsible, being an act, neglect or default in the navigation or management of the ship, in the loading, carriage or discharge of goods on, in or from the ship, or in the embarkation, carriage or disembarkation of persons on, in or from the ship; (g) any claim for loss of or damage to goods carried in a ship; (h) any claim arising out of any agreement relating to the carriage of goods in a ship or to the use or hire of a ship; (i) any claim— (i) under the Salvage Convention 1989; (ii) under any contract for or in relation to salvage services; or (iii) in the nature of salvage not falling within subparagraph (i) or (ii); or any corresponding claim in connection with an aircraft; (j) any claim in the nature of towage in respect of a ship or an aircraft; (k) any claim in the nature of pilotage in respect of a ship or an aircraft; (l) any claim in respect of goods or materials supplied to a ship for her operation or maintenance; (m) any claim in respect of the construction, repair or equipment of a ship or in respect of dock charges or dues; (n) any claim by a master or member of the crew of a ship for wages (including any sum allotted out of wages or adjudged by a superintendent to be due by way of wages); (o) any claim by a master, shipper, charterer or agent in respect of disbursements made on account of a ship; (p) any claim arising out of an act which is or is claimed to be a general average act; (q) any claim arising out of bottomry; (r) any claim for the forfeiture or condemnation of a ship or of goods which are being or have been carried, or have been attempted to be carried, in a ship, or for the restoration of a ship or any such goods after seizure, or for droits of Admiralty; (s) any claim arising under section 7 of the Merchant Shipping (Prevention and Control of Pollution) Ordinance ( Cap. 413 ). (3) The proceedings referred to in subsection (1)(b) are— (a) any application to the Court of First Instance under— (i) the Merchant Shipping Acts 1894 to 1979 # in their application to Hong Kong; (ii) the Merchant Shipping Ordinance ( Cap. 281 ); (iii) the Merchant Shipping (Safety) Ordinance ( Cap. 369 ); (iv) the Merchant Shipping (Liability and Compensation for Oil Pollution) Ordinance ( Cap. 414 ); (v) the Merchant Shipping (Registration) Ordinance ( Cap. 415 ); (vi) the Merchant Shipping (Limitation of Shipowners Liability) Ordinance ( Cap. 434 ); (vii) the Merchant Shipping (Local Vessels) Ordinance ( Cap. 548 ); or (viii) the Bunker Oil Pollution (Liability and Compensation) Ordinance ( Cap. 605 ); (b) any action to enforce a claim for damage, loss of life or personal injury arising out of— (i) a collision between ships; (ii) the carrying out of or omission to carry out a manoeuvre in the case of 1 or more of 2 or more ships; or (iii) non-compliance, on the part of 1 or more of 2 or more ships, with the collision regulations; (c) any action by shipowners or other persons under— (i) the Merchant Shipping Acts 1894 to 1979 # in their application to Hong Kong; (ii) (iii) the Merchant Shipping (Safety) Ordinance ( Cap. 369 ); (iv) the Merchant Shipping (Liability and Compensation for Oil Pollution) Ordinance ( Cap. 414 ); (v) the Merchant Shipping (Limitation of Shipowners Liability) Ordinance ( Cap. 434 ); (vi) the Merchant Shipping (Local Vessels) Ordinance ( Cap. 548 ); or (vii) the Bunker Oil Pollution (Liability and Compensation) Ordinance ( Cap. 605 ), for the limitation of the amount of their liability in connection with a ship or other property. (4) The jurisdiction of the Court of First Instance under subsection (2)(b) includes power to settle any account outstanding and unsettled between the parties in relation to the ship, and to direct that the ship, or any share thereof, shall be sold, and to make such other order as the court thinks fit. (5) Subsection (2)(e) extends to— (a) any claim in respect of a liability incurred under Part II of the Merchant Shipping (Liability and Compensation for Oil Pollution) Ordinance ( Cap. 414 ); (b) any claim in respect of a liability incurred by the International Oil Pollution Compensation Fund under Part III of that Ordinance; and (c) any claim in respect of a liability incurred under section 5 of the Bunker Oil Pollution (Liability and Compensation) Ordinance ( Cap. 605 ). (6) In subsection (2)(i) — (a) the Salvage Convention 1989 ( 1989年救助公約 ) means the International Convention on Salvage 1989 as it has effect under section 9 of the Merchant Shipping (Collision Damage Liability and Salvage) Ordinance ( Cap. 508 ); (b) the reference to salvage services includes services rendered in saving life from a ship and the reference to any claim under any contract for or in relation to salvage services includes any claim arising out of such a contract whether or not arising during the provision of the services; (c) the reference to a corresponding claim in connection with an aircraft is a reference to any claim corresponding to any claim mentioned in subsection (2)(i)(i) or (ii) which is available under section 9 of the Civil Aviation Ordinance ( Cap. 448 ). (7) Subsections (1) to (6) apply— (a) in relation to all ships or aircraft, whether British or not and whether registered or not and wherever the residence or domicile of their owners may be; (b) in relation to all claims, wherever arising (including, in the case of cargo or wreck salvage, claims in respect of cargo or wreck found on land); and (c) so far as they relate to mortgages and charges, to all mortgages or charges, whether registered or not and whether legal or equitable, including mortgages and charges created under foreign law. (8) Nothing in subsection (7) shall be construed as extending the cases in which money or property is recoverable under any of the provisions of— (a) the Merchant Shipping Acts 1894 to 1979 # in their application to Hong Kong; (b) the Merchant Shipping Ordinance ( Cap. 281 ); (ba) the Merchant Shipping (Seafarers) Ordinance ( Cap. 478 ); (c) the Merchant Shipping (Safety) Ordinance ( Cap. 369 ); (d) the Merchant Shipping (Liability and Compensation for Oil Pollution) Ordinance ( Cap. 414 ); (e) the Merchant Shipping (Registration) Ordinance ( Cap. 415 ); (f) the Merchant Shipping (Limitation of Shipowners Liability) Ordinance ( Cap. 434 ); (g) the Merchant Shipping (Local Vessels) Ordinance ( Cap. 548 ); or (h) the Bunker Oil Pollution (Liability and Compensation) Ordinance ( Cap. 605 ). [cf. 1981 c. 54 s. 20 U.K.] Editorial Note: # Please also see following— (a) in relation to the Merchant Shipping Act 1894, Part 3 of Schedule 5 to Cap. 415 and s. 1 of Schedule 2 to Cap. 508 ; (b) in relation to the Merchant Shipping Acts 1894 to 1979, s. 117 of Cap. 281 , s. 103 of Cap. 415 and s. 142 of Cap. 478 ."

system_prompt = """
The user will provide a section of the Hong Kong Legislation document. Your job is to extract the cross references in the section. A cross reference is a reference to another section or schedule in the legislation (Legislation document can appreviated as Cap). For example, "section 31 of Cap. 401". If Cap is not given then it is the current Cap. You should output the cross references in a JSON array.

EXAMPLE JSON OUTPUT:
{
    "refs": [
        {"type": "section", "value": "31", "cap": "401", "subsection": null},
        {"type": "section", "value": "32", "cap": "401A", "subsection": "(1)"}
    ]
}
"""

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Cap. 4, Section 12A: \n\n" + text}
    ]
    kwags = {
        "temperature": 0.5,
        "response_format": {'type': 'json_object'}
    } 
    reasoning_content, content = chatCompletion(messages, kwargs=kwags)

    print(reasoning_content)
    print("-----Response------")
    print(content)