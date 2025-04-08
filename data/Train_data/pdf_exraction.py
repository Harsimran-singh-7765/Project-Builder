

import os
import fitz


import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "Train_data", "Synopsis.pdf")
file_path = os.path.abspath(file_path)

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()


def data_pdf(): 
    file_path = r"data\Train_data\Synopsis.pdf"
    data = extract_text_from_pdf(file_path)
    return data

