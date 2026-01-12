from pypdf import PdfReader
from docx import Document
import requests
from bs4 import BeautifulSoup

def read_pdf(path):
    reader = PdfReader(path)
    return [page.extract_text() for page in reader.pages if page.extract_text()]

def read_docx(path):
    doc = Document(path)
    return [p.text for p in doc.paragraphs if p.text.strip()]

def read_url(url):
    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    return [soup.get_text(separator=" ")]
