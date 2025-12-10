import pdfplumber
import openpyxl
from openpyxl import Workbook
import re
from pathlib import Path

def extract_hymn_info(pdf_path):                                #Extract hymn info from a single file
    results = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"         #extract text from all pages, and add a new line between pages

            filename = Path(pdf_path).stem                      #extract date from filename: filename format is "YYYYMMDD - LIEDERE.pdf"
            date_match = re.search(r'(\d{8})', filename)
            date = date_match.group(1) if date_match else filename

            if len(date) == 8 and date.isdigit():               #checks if date is 8 characters and all digits, then formats date as YYYY-MM-DD
                date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
            
            headings = [                                        #define headings to look for
                'Antwoord', 'Familienuus', 'Gebedsmoment', 
                'Lied', 'Loflied', 'Offergawe', 'Seën', 'Seëngroet', 
                'Skriflesing', 'Slotlied', 'Stilgebed', 'Toetrede', 
                'Voorsang', 'Votum', 'Wydingslied'
            ]
            