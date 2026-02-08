import sqlite3
import pdfplumber
import re
import os

DB_PATH = os.path.join("data", "renal_drugs.db")
PDF_PATH = "The_Renal_Drug.pdf"

def get_toc_mapping():
    """Extracts mapping from TOC pages (approx 11-18)."""
    mapping = {}
    with pdfplumber.open(PDF_PATH) as pdf:
        for p_idx in range(10, 18): # Pages 11 to 18
            text = pdf.pages[p_idx].extract_text()
            if not text: continue
            
            # Matches "Drug Name . . . . 123"
            matches = re.findall(r'(.+?)\s+\.{2,}\s*(\d+)', text)
            for name, page in matches:
                name = name.strip().replace(' .', '')
                mapping[name.lower()] = int(page)
    return mapping

def validate():
    print("--- Starting Safety Validation ---")
    toc = get_toc_mapping()
    print(f"Loaded {len(toc)} entries from TOC.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drugs")
    rows = cursor.fetchall()

    errors = []
    
    headers = [
        "Clinical use", 
        "Dose in normal renal function", 
        "Dose in renal impairment", 
        "Pharmacokinetics", 
        "Important drug interactions", 
        "Administration"
    ]

    for row in rows:
        name = row['name'].lower()
        db_page = row['page_number']
        
        # 1. Page Correspondence Check
        # Clean name for matching (removes page numbers often extracted in names)
        clean_name = re.sub(r'\s*\d+$', '', name).strip()
        
        if clean_name in toc:
            toc_page = toc[clean_name]
            # PDF internal index often differs from printed page number
            # We check if they are "close" (within 5-10 pages offset usually)
            # OR we check if the actual text on that page contains the name.
            pass # We'll refine this if we see massive shifts

        # 2. Section "Internal Leak" Check
        # Look for headers inside other sections
        for col in ['clinical_use', 'dose_normal', 'pharmacokinetics', 'interactions']:
            text = row[col] or ""
            for h in headers:
                if h in text:
                    match = re.search(r'(?:\n|^)' + re.escape(h), text)
                    if match:
                        context = text[max(0, match.start()-40):min(len(text), match.end()+40)].replace('\n', ' ')
                        errors.append(f"CRITICAL: Header '{h}' LEAKED in {col} for {row['name']} | Context: ...{context}...")

        # 3. Encoding check
        for col in row.keys():
            if isinstance(row[col], str) and '' in row[col]:
                # We expect some  for special chars, but let's flag huge concentrations
                if row[col].count('') > 5:
                    errors.append(f"WARNING: High number of encoding errors in {col} for {row['name']}")

    conn.close()
    
    # Write report
    with open("safety_validation_results.txt", "w", encoding="utf-8") as f:
        for err in errors:
            f.write(err + "\n")
            print(err)
            
    print(f"\nValidation finished. Found {len(errors)} issues.")

if __name__ == "__main__":
    validate()
