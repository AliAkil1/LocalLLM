import requests
from bs4 import BeautifulSoup
import PyPDF2

def truncate_text(text, max_length=8000):
    """Truncate text to a maximum length while keeping whole sentences"""
    if len(text) <= max_length:
        return text
    
    # Find the last sentence boundary before max_length
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    if last_period != -1:
        return text[:last_period + 1]
    return truncated

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return truncate_text(text)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def scrape_website(url):
    """Scrape and clean web content"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text and clean it
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return truncate_text(text)
    except Exception as e:
        return str(e) 