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

    query_vector = np.array([vector]).astype("float32") # reshaping into 2d matrix FAISS
    distances, indices = INDEX.search(query_vector, k = 5) # searching the index and returning top 5 matches

    results = [] # retrieving actual text 
    for i in indices[0]:
        if i != -1:
            results.append(METADATA[i])

    return results


def generate_answer(query, context):
    context_str = "\n\n".join([f"Source (Page {c['page']}): {c['text']}" for c in context])

    # system's rules
    system_prompt = {
        "You are Eliza, a helpful financial analyst for BNY Mellon. "
        "Answer the user's question based ONLY on the provided context below. "
        "If the answer is not in the context, say 'I cannot find that information in the documents.' "
        "Keep your answer professional and concise."
    }

    # User prompt:
    user_message = f"Context:\n{context_str}\n\nQuestion: {query}"

    # calling openAI
    response = client.chat.completions.create(
        model="gpt-4o",
        message=[
            {"role", "system", "content", system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

if __name__ == "__main__":
    pass