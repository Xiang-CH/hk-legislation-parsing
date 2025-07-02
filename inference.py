from openai import OpenAI
import json

MODEL = "deepseek-r1-distill-qwen-32b"
client = OpenAI(
    base_url="http://localhost:5000/v1",
    api_key="EMPTY"
)
with open("ref_parsing/system_prompt.md", "r") as f:
    system_prompt = f.read()

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



def createPrompt(cap, section, subsection, text):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Cap. {cap}, Section {section}, Subsection ({subsection}): \n\n{text}" if subsection else f"Cap. {cap}, Section {section}: \n\n{text}"}
    ]

def getReference(cap, section, subsection, text):
    messages = createPrompt(cap, section, subsection, text)
    kwags = {
        "temperature": 0.6,
        "response_format": {'type': 'json_object'}
    } 
    reasoning_content, content = chatCompletion(messages, kwargs=kwags)
    return json.loads(content)['refs']



if __name__ == "__main__":
    text = "### (1) On and from the appointed day, by virtue of this Ordinance and notwithstanding the provisions of any other Ordinance—\n\t(a) the balance sheets and profit and loss accounts of MEFIL and Emirates Bank for the accounting period of each company in which the appointed day falls shall be prepared in all respects as if the undertaking had vested in Emirates Bank pursuant to section 5 on the first day of such accounting period of MEFIL;\n\t(b) every existing provision against assets of MEFIL shall be transferred to and for all purposes be and become a provision against assets of Emirates Bank; and\n\t(c) the amount, description and character of every provision of Emirates Bank which shall come into being pursuant to paragraph (b) shall be the same in all respects as those of the corresponding existing provision immediately before such appointed day, and all enactments and rules of law shall apply to or in respect of every such provision of Emirates Bank in the same manner in all respects as they applied to or in respect of the corresponding existing provision immediately before the appointed day."
    messages = createPrompt(1154, 8, 1, text)
    kwags = {
        "temperature": 0.6,
        "response_format": {'type': 'json_object'}
    } 
    reasoning_content, content = chatCompletion(messages, kwargs=kwags)

    print(reasoning_content)
    print("-----Response------")
    print(content)