# loads 'all_master_chunks.json'
# downloads pre-trained AI 
# Convert every text chunk into a list of 1536 numbers (vectors)
# Saves vectors into a FAISS index 

import openai
import json
import pathlib
import os
import numpy as np # Matrix math library 
import faiss    # Vector database library 
from tqdm import tqdm # Progress bar 

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
    
    output_dir = DATA_DIR / "vector_db" # checks if the vector database exist, if not, create it 
    if not output_dir.exists(): 
        output_dir.mkdir(parents=True)

    with open(input_file, 'r') as f:
        chunks = json.load(f)

    vector_list = []
    metadata_list = []

    for item in tqdm(chunks): # tqdm wraps the list to show a progress bar in terminal 
        try:
            vector = get_embedding(item['text'])
            vector_list.append(vector)
            metadata_list.append(item)
        except Exception as e:
            print(f"Skipping chunk due to error: {e}")

    vectors = np.array(vector_list).astype('float32') # np.array converts list of lists into a matrix 

    # building the database
    dimension = 1536
    # IndexFlatL2 -> when search, calculate distance between vectors to find closest match 
    index = faiss.IndexFlatL2(dimension) # creating an empty database expecting 1536 - dim vectors
    index.add(vectors) # Add matrix to database 
    faiss.write_index(index, str(output_dir / "eliza.index"))
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata_list, f)
