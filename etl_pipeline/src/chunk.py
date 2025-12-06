# load raw data
# clean data 
# chunk the text

import json
import os
import pathlib
import re  # New friend: Regular Expressions

current_dir = pathlib.Path(__file__).parent
DATA_DIR = current_dir.parent.parent / "data" 

def clean_text(text):
    # Remove Page Numbers (e.g., "Page 15" or just "15" on a new line)
    # Pattern: \n (newline) + \d+ (one or more digits) + \n (newline)
    text = re.sub(r'\n\d+\n', '\n', text)
    
    # Remove "Page X of Y" artifacts
    # Pattern: Page + space + digits + space + of + space + digits
    text = re.sub(r'Page \d+ of \d+', '', text)
    
    # Remove Table of Contents dots (e.g., "Item 1....................... 55")
    # Pattern: 4 or more dots in a row
    text = re.sub(r'\.{4,}', '', text)
    
    # Collapse multiple newlines (The "Whitespace" fix)
    # Pattern: 3 or more newlines becomes 2 newlines (paragraph break)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()

def chunk_text(text, target_word_count = 200, overlap = 20): # function that will chunk the text 
    split_text = text.split() # splitting text into list of words
    chunks = [] # list to hold chunk
    step = target_word_count - overlap # calculating each 'step' 
    for i in range(0, len(split_text), step): # looping through the split_text list 
        chunk_end = i + target_word_count # calculating the end of a chunk 
        chunk_words = split_text[i : chunk_end] # establishing the current chunk of words from i -> the calculated end of chunk 
        chunk_string = " ".join(chunk_words) # join the different strings into one long string 
        chunks.append(chunk_string) # append that string into the chunks list 
    return chunks # return the list of chunks 


if __name__ == "__main__":
    input_folder = DATA_DIR / "processed" 
    all_chunks = [] # master list to store all of the chunks 

    file_data = list(input_folder.glob("*.json")) # getting a list of all the .json files in the processed folder

    for file_path in file_data: # looping through the file paths 

        with open(file_path, 'r', encoding="utf-8") as f: # open and load the file
            current_file_page = json.load(f)

        for page_item in current_file_page:
            text_to_clean = page_item['text']
            cleaned_text = clean_text(text_to_clean)
            chunked_text = chunk_text(cleaned_text)

            for i, chunk_string in enumerate(chunked_text):
                record = {
                    "id": f"{page_item['source']}_{page_item['page']}_{i}",
                    "text": chunk_string,
                    "page": page_item['page'],
                    "source": page_item['source']
                }
                all_chunks.append(record)

    output_file = DATA_DIR / "processed" / "all_master_chunks.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=4)

    
