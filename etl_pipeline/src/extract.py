import pymupdf
import pathlib
import json
import os

current_dir = pathlib.Path(__file__).parent # getting path to this script (etl_pipeline/src/)
DATA_DIR = current_dir.parent.parent / "data" # getting path to the directory where the data lives 

def extract_text_from_pdf(file_path):
    extracted_data = [] 
    doc = pymupdf.open(file_path) # creating a document object that will hold meta-data of PDF 
    for index, page in enumerate(doc): # for loop to go through each page of the document and extract the text 
        text = page.get_text()
        page_data = {
            "page": index + 1,       
            "text": text,
            "source": os.path.basename(file_path)
        }
        extracted_data.append(page_data)

    return extracted_data

if __name__ == "__main__":
    test_file = DATA_DIR / "raw" / "nvidia_10K.pdf" 
    
    print(f"Processing {test_file}...")
    data = extract_text_from_pdf(test_file)
    
    # 3. Print results to prove it worked
    print(f"Success! Extracted {len(data)} pages.")
    print("Preview of Page 1:", data[0]['text'][:100])






