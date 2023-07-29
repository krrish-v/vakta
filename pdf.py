# pip install pdfminer.six
from pdfminer.high_level import extract_pages,extract_text

text = extract_text("sample.pdf")
print(text)