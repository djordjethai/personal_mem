from openai import OpenAI
from pinecone.grpc import PineconeGRPC as Pinecone
import os
from datetime import datetime
import json

client = OpenAI()

# Initialize Pinecone
index_name="memory" #opsti index za memoriju
pc=Pinecone(api_key=os.environ.get("PINECONE_API_KEY"), host='https://memory-a9w1e6k.svc.aped-4627-b74a.pinecone.io') #memory (djordje, standard)
index = pc.Index(name=index_name, host='https://memory-a9w1e6k.svc.aped-4627-b74a.pinecone.io') #memory semantic
user_id = "test01" # konkretan prijavljeni user
namespace = "razvoj01" # konkretni klijent (firma)
current_date = datetime.now()
date_string = current_date.strftime('%Y%m%d')

# Function to save personal facts using Pinecone
def save_facts(user_input, user_id, namespace, fact_type):
    # Step 1: Extract a concise personal fact using OpenAI GPT
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Write only relevant fact from this text '{user_input}' concisely."}]
    )
    fact = response.choices[0].message.content

    # Step 2: Embed the fact using OpenAI Embedding API (512 dimensions)
    embedding = client.embeddings.create(input = [fact], dimensions=512, model="text-embedding-3-small").data[0].embedding

    # Step 3: Check if the fact already exists using Pinecone
    query_response = index.query(
        vector=embedding,
        namespace=namespace,
        top_k=1,
        filter={"user_id": user_id, "type": fact_type},
        include_metadata=True
    )
    
    # If no similar facts are found (based on a similarity threshold)
    if not query_response['matches'] or query_response['matches'][0]['score'] < 0.85:
        # Step 4: Store the new fact in Pinecone with metadata
        index.upsert(namespace=namespace,
            vectors=[{
                "id": f"{user_id}_{fact_type}_{len(query_response['matches']) + 1}",
                "values": embedding,
                "metadata": {
                    "text": fact,
                    "user_id": user_id,
                    "type": fact_type,
                    "date": int(date_string)
                }
            }]
        )
        print(f"New fact '{fact}' added to Pinecone.")
    else:
        print(f"The fact '{fact}' already exists.")

def retrieve_facts(query, user_id, namespace, fact_type):
    # Step 1: Embed the query using OpenAI Embedding API
    query_embedding = client.embeddings.create(input = [query], dimensions=512, model="text-embedding-3-small").data[0].embedding
    
    # Step 2: Search for personal facts in Pinecone using metadata filter and similarity
    query_response = index.query(
        vector=query_embedding,
        namespace=namespace,
        top_k=5,
        filter={"user_id": user_id, "type": fact_type},
        include_metadata=True
    )
    
    # Step 3: Process and return the retrieved facts
    if query_response['matches']:
        personal_facts = [match['metadata']['text'] for match in query_response['matches'] if match['score'] >= 0.1]
    else:
        personal_facts = "I don't know"    
    return personal_facts


# Define the functions for the assistant to call
tool_list = [
    {   "type": "function",
           "function": {
                "name": "save_facts",
                "description": "Extracts facts and saves them to a JSON file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "facts": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of facts."
                        },
                        "fact_type": {
                            "type": "string",
                            "enum": ["personal", "business", "other"],
                            "description": "List of fact types (personal, business, other)."
                        },
                    },
            "required": ["facts", "fact_type"],
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

# Process function calls in a loop
if response.choices[0].message.tool_calls is not None:
    for tool_call in response.choices[0].message.tool_calls:

        if tool_call.function.name == 'save_facts':
                fact_dict = json.loads(tool_call.function.arguments)
                fact_type= fact_dict['fact_type']
                save_facts(user_input, user_id, namespace, fact_type)
                print("!!!!!!!!!")
                print(f"Facts upserted: type: {fact_dict["fact_type"]} fact: {fact_dict["facts"]}")
                


else:
    print("No tools selected!")       



ret_tool_list = [
    {   "type": "function",
           "function": {
                "name": "retrieve_facts",
                "description": "Retrieves facts about me.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "facts": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of facts."
                        },
                        "fact_type": {
                            "type": "string",
                            "enum": ["personal", "business", "other"],
                            "description": "List of fact types (personal, business, other)."
                        },
                    },
            "required": ["facts", "fact_type"],
        },
    }},
]

ret_response = client.chat.completions.create(
    model="gpt-4o-mini",  # or another model you prefer
    messages=messages,
    tools=ret_tool_list,
    tool_choice='required'
    
)

print("")
print("_______________________")
print("Retrieval.....")
print("")
ret_facts = []
if ret_response.choices[0].message.tool_calls is not None:
    for tool_call in ret_response.choices[0].message.tool_calls:
        if tool_call.function.name == 'retrieve_facts':
            fact_dict = json.loads(tool_call.function.arguments)
            fact_type= fact_dict['fact_type']
            ret_facts.append(retrieve_facts(user_input, user_id, namespace, fact_type))
            print("!!!!!!!!!")
            print(f"Facts retrieved: fact type: {fact_dict["fact_type"]} fact: {fact_dict["facts"]}")
           
            
else:
    print("No tools selected!")       

prompt = f"""
    Please answer the question {user_input} based on this context {ret_facts}
    """
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
    {"role": "user", "content": prompt}
],
    )
answer = response.choices[0].message.content
print("")
print("_______________")
print(answer)
print("_______________")
