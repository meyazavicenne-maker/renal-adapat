import re

def parse_drug_dosages(drug):
    """
    Parses drug dosage information into a structured list of rows.
    Returns: List of {"category": str, "recommendation": str}
    """
    rows = []
    dialysis_keys = sorted(["APD/CAPD", "HD", "HDF/High flux", "CAV/VVHD"], key=len, reverse=True)
    
    # 1. Parse GFR (Renal Impairment)
    renal_text = drug.get("dose_renal_impairment")
    if renal_text:
        lines = renal_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Skip header-like lines
            clean_line = line.upper()
            if clean_line in ["GFR (ML/MIN)", "RENAL IMPAIRMENT"]:
                continue

            # Pattern: Start with GFR range
            match = re.match(r'^((?:>|<)?\s*\d+(?:[-–\u2013\u2014\ufffd]\d+)?(?:\s*mL/min)?)\s+(.*)', line, re.IGNORECASE)
            if match:
                gfr_range = match.group(1).strip()
                recommendation = match.group(2).strip()
                
                # Validation: contains digit
                is_valid_gfr = any(c.isdigit() for c in gfr_range)
                
                if is_valid_gfr:
                    # Split recommendation into sub-parts (Dose + Dialysis + Warnings)
                    sub_rows = _split_by_keys_and_bullets(recommendation, initial_cat=f"GFR {gfr_range}")
                    
                    if sub_rows:
                        # The first part is the GFR recommendation
                        first_row = sub_rows[0]
                        rows.append({"category": f"GFR {gfr_range}", "recommendation": first_row["recommendation"]})
                        rows.extend(sub_rows[1:])
                    else:
                        rows.append({"category": f"GFR {gfr_range}", "recommendation": recommendation})
            else:
                # Check if line starts with a Dialysis key
                found_key = None
                for k in dialysis_keys:
                    if line.upper().startswith(k.upper()):
                        found_key = k
                        break
                
                if found_key:
                    content = line[len(found_key):].strip()
                    # Add row for key, then split its content
                    rows.append({"category": found_key, "recommendation": ""})
                    sub_rows = _split_by_keys_and_bullets(content, initial_cat=found_key)
                    if sub_rows:
                        if sub_rows[0]["category"] == found_key and not rows[-1]["recommendation"]:
                             rows[-1]["recommendation"] = sub_rows[0]["recommendation"]
                             rows.extend(sub_rows[1:])
                        else:
                             rows.extend(sub_rows)
                elif rows:
                    # Potential continuation, but first check for internal keys/bullets
                    # Pass the category of the LAST row as the context
                    last_cat = rows[-1]["category"]
                    sub_rows = _split_by_keys_and_bullets(line, initial_cat=last_cat)
                    if sub_rows:
                        # If the first sub_row matches the last category, it's a real continuation
                        if sub_rows[0]["category"] == last_cat:
                             rows[-1]["recommendation"] += f" {sub_rows[0]['recommendation']}"
                             rows.extend(sub_rows[1:])
                        else:
                             rows.extend(sub_rows)
                    else:
                        rows[-1]["recommendation"] += f" {line}"
                else:
                    # Fallback row
                    rows.append({"category": "Note", "recommendation": line})

    # 2. Parse Dialysis (Replacement Therapy)
    replacement_text = drug.get("dose_replacement")
    if replacement_text:
        keys = dialysis_keys
        lines = replacement_text.split('\n')
        current_cat = "Note" # Default to Note for replacement therapy
        buffer = []
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            found_key = None
            for key in keys:
                if line.upper().startswith(key.upper()):
                    found_key = key
                    break
            
            if found_key:
                if current_cat:
                    content_str = " ".join(buffer)
                    sub_rows = _split_by_keys_and_bullets(content_str, initial_cat=current_cat)
                    if sub_rows:
                        if sub_rows[0]["category"] == current_cat:
                            rows.append({"category": current_cat, "recommendation": sub_rows[0]["recommendation"]})
                            rows.extend(sub_rows[1:])
                        else:
                            rows.append({"category": current_cat, "recommendation": ""})
                            rows.extend(sub_rows)
                
                current_cat = found_key
                content = line[len(found_key):].strip()
                buffer = [content] if content else []
            else:
                if current_cat:
                    buffer.append(line)
        
        if current_cat:
            content_str = " ".join(buffer)
            sub_rows = _split_by_keys_and_bullets(content_str, initial_cat=current_cat)
            if sub_rows:
                if sub_rows[0]["category"] == current_cat:
                    rows.append({"category": current_cat, "recommendation": sub_rows[0]["recommendation"]})
                    rows.extend(sub_rows[1:])
                else:
                    rows.append({"category": current_cat, "recommendation": ""})
                    rows.extend(sub_rows)
            else:
                rows.append({"category": current_cat, "recommendation": ""})

    # 3. Parse Interactions column
    interactions_text = drug.get("interactions")
    if interactions_text:
        # Skip generic header if present
        header = "Potentially hazardous interactions with other drugs"
        if interactions_text.strip().startswith(header):
            interactions_text = interactions_text.strip()[len(header):].strip()
        
        sub_rows = _split_by_keys_and_bullets(interactions_text, initial_cat="Interactions")
        rows.extend(sub_rows)

    # 4. Parse Administration and Others
    for field in ["administration", "other_info"]:
        text = drug.get(field)
        if text:
            sub_rows = _split_by_keys_and_bullets(text, initial_cat="Note")
            rows.extend(sub_rows)
            
    return rows

def _split_by_keys_and_bullets(text, initial_cat="Note"):
    """
    Splits a recommendation string into sub-rows based on internal keys or bullets.
    """
    if not text: return []
    
    dialysis_keys = ["APD/CAPD", "HD", "HDF/High flux", "CAV/VVHD"]
    interrupt_names = ["Important", "Note", "Interactions", "Comments", "Warning"]
    bullet_markers = ["\u2022", "•", "\ufffd"]
    
    # Combined search keys, longest first
    all_keys = sorted(dialysis_keys + interrupt_names, key=len, reverse=True)
    
    # Use word boundaries for keys unless they contain non-word characters like /
    name_patterns = []
    for k in all_keys:
        if "/" in k:
            name_patterns.append(re.escape(k))
        else:
            name_patterns.append(r'\b' + re.escape(k) + r'\b')
            
    name_pattern = r'|'.join(name_patterns)
    bullet_pattern = r'(?<!\d)[' + ''.join(bullet_markers) + r'](?!\d)'
    
    # Combined pattern: Optional bullet + Name OR standalone Bullet
    combined_pattern = r'(?:(?:' + bullet_pattern + r')?\s*(?:' + name_pattern + r')|' + bullet_pattern + r')'
    full_pattern = r'(' + combined_pattern + r')'
    
    # Split
    parts = re.split(full_pattern, text, flags=re.IGNORECASE)
    
    results = []
    active_cat = initial_cat
    
    # Leading text
    if parts[0].strip():
        # If parts[0] is from the very start, it belongs to initial_cat
        # But categorization might change if keywords are found.
        results.append({"category": active_cat, "recommendation": parts[0].strip()})
        
    for i in range(1, len(parts), 2):
        key_text = parts[i].strip()
        val_text = parts[i+1].strip()
        if not key_text: continue
        
        # Identify if we found a known name
        found_name = None
        key_upper = key_text.upper()
        
        for k in all_keys:
            clean_key = re.sub(bullet_pattern, '', key_text).strip().upper()
            if k.upper() == clean_key:
                found_name = k
                break
        
        row_cat = None
        if found_name:
            if found_name in dialysis_keys: 
                active_cat = found_name
            else: 
                active_cat = found_name.title()
            row_cat = active_cat
        else:
            # Standalone bullet marker
            # Heuristic: if we are in an interrupt context, inherit.
            # If we are in Dialysis/GFR context, check for colon (Interactions)
            if active_cat in [n.title() for n in interrupt_names]:
                row_cat = active_cat
            elif ":" in val_text and len(val_text.split(":")[0]) < 30:
                # Likely "Drug: Effect" -> Interaction
                row_cat = "Interactions"
                active_cat = "Interactions" # Update context for subsequent bullets
            else:
                row_cat = "Note"
            
            # Prefix recommendation with bullet for readability
            prefix = "- " if not val_text.startswith("-") and not val_text.startswith("\u2022") else ""
            val_text = f"{prefix}{val_text}"
            
        results.append({"category": row_cat, "recommendation": val_text})
        
    return results
