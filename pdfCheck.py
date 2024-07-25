import os
import sys
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()  # Use extract_text() to get the text of the page
    return text

def find_pdfs_without_trailer(directory):
    pdf_files_without_trailer = []
    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(directory, filename)
            text = extract_text_from_pdf(file_path)
            if 'trailer' not in text.lower():
                pdf_files_without_trailer.append(filename)
    return pdf_files_without_trailer

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdfCheck.py <directory_path>")
        sys.exit(1)
        
    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print("Error: Directory not found.")
        sys.exit(1)

    result = find_pdfs_without_trailer(directory_path)
    print("PDF files without 'trailer':", result)