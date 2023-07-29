
from libser_engine.engine import accumulate, Extract
import random
import os
import  requests
import pdfplumber
import urllib3

def download_pdf_from_link(url):
    urllib3.disable_warnings()
    try:
        output_path = 'pdf/' + str(random.randint(100000, 999999))+'.pdf'
        response = requests.get(url, timeout=5, verify=False, allow_redirects=False)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as file:
                file.write(response.content)
            return output_path
        
        return False
    except: return False


def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    return text

def chunk_string(text):
    chunk_size = 350

    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def get_pdf(subjects):

    extracter = accumulate(query=subjects, filetype='pdf')
    book_link = extracter.all()

    if book_link != []:

        download_book = download_pdf_from_link(book_link[1])
        if download_book is not False:
            doc_text = extract_text_from_pdf(download_book)
            chunked_text = chunk_string(doc_text)
            return chunked_text
