import json

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


with open("system_prompt.md", "r") as f:
    system_prompt = f.read()

def create_prompt(context):
    vars = context['vars']  
    cap = vars['cap']
    section = vars['section']
    subsection = vars['subsection']
    text = vars['text']

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Cap. {cap}, Section {section}, Subsection ({subsection}): \n\n{text}" if subsection else f"Cap. {cap}, Section {section}: \n\n{text}"}
    ]

def call_api(prompt, options, context):
    # Check if prompt is a conversation
    kwags = {
        "temperature": options["temperature"] if "temperature" in options else 0.6,
        "response_format": {'type': 'json_object'}
    } 
    messages = json.loads(prompt)
    # return {
    #     "output": messages
    # }

    reasoning_content, content = chatCompletion(messages, kwargs=kwags)

    return {
        "output": content
    }

# if __name__ == "__main__":
#     text = "### (1) On and from the appointed day, by virtue of this Ordinance and notwithstanding the provisions of any other Ordinance—\n\t(a) the balance sheets and profit and loss accounts of MEFIL and Emirates Bank for the accounting period of each company in which the appointed day falls shall be prepared in all respects as if the undertaking had vested in Emirates Bank pursuant to section 5 on the first day of such accounting period of MEFIL;"
#     reasoning_content, content = test(1154, 8, text, 1)
#     print(reasoning_content)
#     print("-----Response------")
#     print(content)