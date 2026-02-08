import pdfplumber
import sqlite3
import re
import os

PDF_PATH = "The_Renal_Drug.pdf"
DB_PATH = os.path.join("data", "renal_drugs.db")

def save_drug(cursor, drug_data):
    if not drug_data or not drug_data.get("name"):
        return
    
    print(f"Saving: {drug_data['name']}")
    cursor.execute('''
        INSERT INTO drugs (
            name, page_number, clinical_use, dose_normal, 
            dose_renal_impairment, dose_replacement, 
            pharmacokinetics, interactions, administration, other_info
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        drug_data.get("name"),
        drug_data.get("page_number"),
        drug_data.get("clinical_use"),
        drug_data.get("dose_normal"),
        drug_data.get("dose_renal_impairment"),
        drug_data.get("dose_replacement"),
        drug_data.get("pharmacokinetics"),
        drug_data.get("interactions"),
        drug_data.get("administration"),
        drug_data.get("other_info")
    ))
    cursor.connection.commit()

def extract_text_blocks(text):
    data = {}
    
    headers = [
        ("Clinical use", "clinical_use"),
        ("Dose in normal renal function", "dose_normal"),
        ("Dose in renal impairment", "dose_renal_impairment"),
        ("Dose in patients undergoing renal replacement therapies", "dose_replacement"),
        ("Pharmacokinetics", "pharmacokinetics"),
        ("Important drug interactions", "interactions"),
        ("Drug interactions", "interactions"),
        ("Administration", "administration")
    ]
    
    # 1. Find ALL matches for ALL headers
    all_matches = []
    for header, key in headers:
        # Require header to be at the start of a line (after \n or at string start)
        # Allow trailing text on the same line (e.g. "Dose in renal impairment GFR (mL/min)")
        pattern = r'(?:^|\n)\s*' + re.escape(header).replace(r'\ ', r'\s+') + r'[^\n]*?(?:\n|$)'
        for m in re.finditer(pattern, text, re.IGNORECASE):
            all_matches.append({
                'start': int(m.start()),
                'end': int(m.end()),
                'key': str(key),
                'header': str(header),
                'len': int(len(header))
            })
            
    # 2. Sort by start position
    all_matches.sort(key=lambda x: x['start'])
    
    # 3. Resolve Overlaps (keep the longest match if starts are same or close)
    filtered_matches = []
    if all_matches:
        filtered_matches.append(all_matches[0])
        for i in range(1, len(all_matches)):
            curr = all_matches[i]
            prev = filtered_matches[-1]
            
            # If current match is entirely or mostly inside previous, or they overlap significantly
            if curr['start'] < prev['end']:
                # Keep the longer one (or more specific one)
                if curr['len'] > prev['len']:
                    filtered_matches[-1] = curr
                continue
            filtered_matches.append(curr)
            
    # 4. Extract substrings
    for i in range(len(filtered_matches)):
        match = filtered_matches[i]
        start_content = match['end']
        
        if i < len(filtered_matches) - 1:
            end_content = filtered_matches[i+1]['start']
            content = text[start_content:end_content]
        else:
            content = text[start_content:]
            
        data[match['key']] = content.strip()
        
    return data

def extract_all():
    # Initialize DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    current_drug = None
    
    with pdfplumber.open(PDF_PATH) as pdf:
        total_pages = len(pdf.pages)
        print(f"Processing {total_pages} pages...")
        
        # Start from page 11 (Index 10) where Abacavir is found
        start_page_index = 10 
        
        for i in range(start_page_index, total_pages):
            page = pdf.pages[i]
            page_num = i + 1
            
            width = page.width
            height = page.height
            
            # Dimensions
            header_height = height * 0.15
            mid_point = width / 2
            
            # Zones
            header_bbox = (0, 0, width, header_height)
            left_bbox = (0, 0, mid_point, height)
            right_bbox = (mid_point, 0, width, height)
            
            # Extract Text
            # We fetch the FULL left column to check for "Clinical use", even if it overlaps the header
            full_left_text = page.within_bbox((0, 0, mid_point, height)).extract_text() or ""
            
            header_text = page.within_bbox(header_bbox).extract_text() or ""
            left_text = page.within_bbox(left_bbox).extract_text() or ""
            right_text = page.within_bbox(right_bbox).extract_text() or ""
            
            # Check for New Drug Signals
            # 1. "Clinical use" in Left Column (Case Insensitive)
            is_new_drug = re.search(r"Clinical\s+use", full_left_text, re.IGNORECASE) is not None
            
            if is_new_drug:
                # Save previous drug if exists
                if current_drug:
                    # Parse the accumulated text before saving
                    parsed_data = extract_text_blocks(current_drug["raw_text"])
                    current_drug.update(parsed_data)
                    save_drug(cursor, current_drug)
                
                # Start new drug
                # Clean header to get name
                name_lines = header_text.split('\n')
                name = name_lines[0] if name_lines else f"Drug_Page_{page_num}"
                # Clean up name (remove page numbers if attached, e.g. "32 Aldesleukin")
                name = re.sub(r'^\d+\s+', '', name).strip()
                
                current_drug = {
                    "name": name,
                    "page_number": page_num,
                    # Include header_text so we capture Clinical use if it was in the header
                    "raw_text": left_text + "\n" + right_text
                }
            else:
                # Continuation
                if current_drug:
                    current_drug["raw_text"] += "\n" + left_text + "\n" + right_text
        
        # Save last drug
        if current_drug:
            parsed_data = extract_text_blocks(current_drug["raw_text"])
            current_drug.update(parsed_data)
            save_drug(cursor, current_drug)
            
    conn.commit()
    conn.close()
    print("Extraction Complete.")

if __name__ == "__main__":
    try:
        extract_all()
    except Exception as e:
        print(f"Error: {e}")
