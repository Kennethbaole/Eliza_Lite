# loads 'all_master_chunks.json'
# downloads pre-trained AI 
# Convert every text chunk into a list of 1536 numbers (vectors)
# Saves vectors into a FAISS index 

import openai
import json
import pathlib
import os
import numpy as np
import faiss

# paths
current_dir = pathlib.Path(__file__).parent
DATA_DIR = current_dir.parent.parent / "data"

# client
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def get_embedding(text):
    text = text.replace("\n", " ") # replacing new lines with space 
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding

if __name__ == "__main__":
    input_file = DATA_DIR / "processed" / "all_master_chunks.json"
    # loading chunks 
    with open(input_file, 'r') as f:
        chunks = json.load(f)

    # two buckets:
    vector_list = [] # holds vectors (list of numbers)
    metadata_list = [] # holds text/page info 

    for i, item in enumerate(chunks[:5]):
        vector = get_embedding(item['text']) # item is a dictionary, only extract 'text'
        vector_list.append(vector) # appending vector 
        metadata_list.append(item) # appending the dictionary 
    
    if len(vector_list) > 0:
        print(f"Vector Dimension: {len(vector_list[0])}") # should be 1536
