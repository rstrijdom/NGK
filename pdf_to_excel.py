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
                'Antwoord', 'Gebedsmoment', 
                'Lied', 'Loflied', 'Offergawe', 'Seën',  
                'Skriflesing', 'Slotlied', 'Stilgebed', 'Toetrede', 
                'Voorsang', 'Wydingslied'
            ]
            
            lines = full_text.split('\n')

            for i, line in enumerate(lines):
                for heading in headings:                        #Check if the line contains a heading. 
                    if heading in line:                         #Consider using startswith() if it gives false positives
                        search_text = line
                        for j in range(1, 5):                   #search the next 5 lines for song info - is this necessary?
                            if i + j < len(lines):
                                next_line = lines[i + j]
                                if any(h in next_line for h in headings):
                                    break                       #stop if this line contains another heading
                                search_text += " " + lines[i + j]

                                lb_matches = re.findall(r'LB\s*(\d+)', search_text, re.IGNORECASE)  #extract LB numbers
                                vonkk_matches = re.findall(r'VONKK\s*(\d+)', search_text, re.IGNORECASE) #extract VONKK numbers

                                #also add here a FLAM/Psalm number extractor and a custom list extractor - possibly make a hymn_books variable

                                title_match = re.search(r'(?:LB|VONKK)\s*\d+\s+([^\(]+)', search_text, re.IGNORECASE)
                                title = title_match.group(1).strip() if title_match else ""
