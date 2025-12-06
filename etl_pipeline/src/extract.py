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
    raw_folder = DATA_DIR / "raw"
    processed_folder = DATA_DIR / "processed"

    pdf_files = list(raw_folder.glob("*.pdf")) # getting a list of all the pdfs in the raw folder
    for pdf_path in pdf_files:
        print(f"Processing {pdf_path.name}...")
        data = extract_text_from_pdf(pdf_path) # running extraction function 
        output_filename = f"{pdf_path.stem}.json" # if input = "apple.pdf", output = "apple.json"
        output_path = processed_folder / output_filename

        print(f"Saving to -> {output_filename}...")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    print("Batch processing complete!")





