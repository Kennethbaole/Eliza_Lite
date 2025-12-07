import json
import pathlib
import os
import numpy as np # Matrix math library 
import faiss    # Vector database library 
import openai
from .utils import get_embedding

# Paths
current_dir = pathlib.Path(__file__).parent
DATA_DIR = current_dir.parent.parent / "data"
vector_db_path = DATA_DIR / "vector_db"

# client
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key = api_key)

def load_index():
    global INDEX, METADATA

    input_elizaIndex = vector_db_path / "eliza.index"
    input_metadata = vector_db_path / "metadata.json"

    INDEX = faiss.read_index(str(input_elizaIndex)) # load the index 
    with open(input_metadata, 'r') as f: # load metadata 
        METADATA = json.load(f)

def search(query): # need to search for vector representation, not string 
    vector = get_embedding(query) # user text converted to vector
    query_vector = np.array([vector]).astype("float32")


def generate_answer(query, context):
    pass

if __name__ == "__main__":
    pass