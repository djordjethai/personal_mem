from openai import OpenAI
import json

client = OpenAI()

def save_personal_facts(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "user", "content": f"Write only relevant personal fact from this text {user_input} concisely. Omit pronouns, write the fact only"}
        ])
    facts = response.choices[0].message.content 
    try:
        # Step 1: Read the existing data from the JSON file
        with open('personal_facts.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            # Ensure that the data is a list
            if not isinstance(data, list):
                raise ValueError(f"The JSON data is not a list.")
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        data = []
    except json.JSONDecodeError:
        # If the file is empty or contains invalid JSON, start with an empty list
        data = []

    # Step 2: Append the new item to the list
    exists = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "user", "content": f"Check if {facts} already exists in any form in {data}. Answer only Yes or No"}
        ])
    if_exists = exists.choices[0].message.content 
    print(data)
    print(if_exists)
    if if_exists == "No":
        data.append(facts)
        print("new fact added")
    else:
        print(f"The fact {facts} exists")    

    # Step 3: Write the updated list back to the JSON file
    with open('personal_facts.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def save_business_facts(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "user", "content": f"Write only relevant business fact from this text {user_input} concisely. Omit pronouns, write the fact only"}
        ])
    facts = response.choices[0].message.content 
    try:
        # Step 1: Read the existing data from the JSON file
        with open('business_facts.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            # Ensure that the data is a list
            if not isinstance(data, list):
                raise ValueError(f"The JSON data is not a list.")
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        data = []
    except json.JSONDecodeError:
        # If the file is empty or contains invalid JSON, start with an empty list
        data = []

    # Step 2: Append the new item to the list
    exists = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "user", "content": f"Check if {facts} already exists in any form in {data}. Answer only Yes or No"}
        ])
    if_exists = exists.choices[0].message.content 
    print(data)
    print(if_exists)
    if if_exists == "No":
        data.append(facts)
        print("new fact added")
    else:
        print(f"The fact {facts} exists")    

    # Step 3: Write the updated list back to the JSON file
    with open('business_facts.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def retrieve_personal_facts(query):
    try:
        with open('personal_facts.json', 'r', encoding="utf-8") as f:
            facts = json.load(f)
    except FileNotFoundError:
        return ["No personal facts available."]
   
    if facts:
        return facts
    else:
        return ["No matching personal facts found."]

# Define the functions for the assistant to call
tool_list = [
    {   "type": "function",
           "function": {
                "name": "save_personal_facts",
                "description": "Extracts personal facts and saves them to a JSON file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "facts": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of personal facts."
                        },
                    },
            "required": ["facts"],
        },
    }},
        {  "type": "function",
           "function": {
            "name": "save_business_facts",
            "description": "Extracts business facts and saves them to a JSON file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "facts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of business facts."
                    },
                },
                "required": ["facts"],
            },
    }},
]

user_input = input("Please enter your text: ")

messages = [
    {"role": "user", "content": user_input}
]

# Initial request to the assistant
response = client.chat.completions.create(
    model="gpt-4o-mini",  # or another model you prefer
    messages=messages,
    tools=tool_list,
    tool_choice='auto'
    
)
try:
    izbor = response.choices[0].message.tool_calls[0].function.name
except:
    izbor = "no tools"    

print(izbor)
# Process function calls in a loop

if izbor == 'save_personal_facts':
        save_personal_facts(user_input)
        print("Personal facts saved to personal_facts.json")

print("All facts have been processed.")
personal = retrieve_personal_facts(user_input)

prompt = f"""
    Please answer the question {user_input} based on this context {personal}
    """
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
    {"role": "user", "content": prompt}
],
    )
answer = response.choices[0].message.content
print(answer)
