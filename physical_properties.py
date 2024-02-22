from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}
                ,{"role": "system", "content": "You are a Materials Science and Design Engineering expert."}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


design_choice = [
    "Kitchen Utensil Grip",
    "Spacecraft Component",
    "Underwater Component",
    "Safety Helmet"
]

criterion = [
    "Lightweight",
    "Resistant to Heat",
    "Corrosion Resistant",
    "High Strength"
]

physical_properties = [
    "Young's Modulus", 
    "Density",
    "Yield Strength"
]

def prompt_response(design_choice: str, criterion: str):
    prompt = f"""
    You are given a problem statement to assist a designer as below:
    The information below is provided to you delimited by triple backticks

    Design: '''{design_choice}'''
    Criterion: '''{criterion}'''

    You are tasked with designing the grip of {design_choice} which should be {criterion}.
    
    Suggest the optimal physical properties of a material that satisfies the case above?

    As a materials science and design engineer with experience in this field, 
    you are supposed to give physical properties of the most optimal material which satisfies {criterion} for the {design_choice}.
    The physical properties should be in a min-max range and the physical properties to suggest are '''{physical_properties}'''.
    
    The properties are intended on a viability perspective, so the focus should be on how well the material satisfies the design and criterion pair.

    Output should be of a JSON format, use the following format:

    Output JSON:
    (
    'design' : {design_choice},
    'criterion' : {criterion},
    'material' : suggested material,
    'physical property 1 (As shown in the input above)' : ('min': minimum value of physical property 1 (keep only the numeric value and no units),
    'max': maximum value of physical property 1 (keep only the numeric value and no units),
    'units':units of measurement for values)
    ...
    ...
    )
    """


    response = get_completion(prompt)

    # print(f"\n Response Range: \n")
    # print(response)
    return response

# score_json = prompt_response(design_choice[0], criterion[0])

# for i in range(len(materials)):
for j in range(len(design_choice)):
    for k in range(len(criterion)):
        range_json = prompt_response(design_choice[j], criterion[k])

#         print(f"Output {j}",score_json)

        path = f"/Users/yashpatawari/LLM_Materials/Properties/{design_choice[j]}_{criterion[k]}_Range"

        with open(path, "w") as json_file:
            json.dump(range_json, json_file)
            print(f"Data Saved to {path}")




# path = "steel_single.json"

# with open(path, "w") as json_file:
#     json.dump(response, json_file)

# print(f"Data saved to {path}")
