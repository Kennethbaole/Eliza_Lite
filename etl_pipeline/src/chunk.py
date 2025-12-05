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
    # 1. Remove Page Numbers (e.g., "Page 15" or just "15" on a new line)
    # Pattern: \n (newline) + \d+ (one or more digits) + \n (newline)
    text = re.sub(r'\n\d+\n', '\n', text)
    
    # 2. Remove "Page X of Y" artifacts
    # Pattern: Page + space + digits + space + of + space + digits
    text = re.sub(r'Page \d+ of \d+', '', text)
    
    # 3. Remove Table of Contents dots (e.g., "Item 1....................... 55")
    # Pattern: 4 or more dots in a row
    text = re.sub(r'\.{4,}', '', text)
    
    # 4. Collapse multiple newlines (The "Whitespace" fix)
    # Pattern: 3 or more newlines becomes 2 newlines (paragraph break)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()

if __name__ == "__main__":
    input_file = DATA_DIR / "processed" / "nvidia_10k_raw.json"

    # loading the data 
    with open(input_file, 'r') as f:
        raw_data = json.load(f)

    # cleaning the text 
    sample_text = raw_data[0]['text']

    print(" -- Before -- ")
    print(sample_text[:500])

    cleaned_sample = clean_text(sample_text)
    print("\n--- After ---")
    print(cleaned_sample[:500])