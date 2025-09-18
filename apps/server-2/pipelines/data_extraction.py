import re

def extract_certificate_data(text):
    """
    Extract key fields (name, roll number, grades).
    """
    data = {}
    roll_match = re.search(r"ROLL\s*NO\.*\s*:\s*(\w+)", text, re.I)
    name_match = re.search(r"NAME\s*:\s*([A-Z\s]+)", text, re.I)
    
    if roll_match:
        data["roll_number"] = roll_match.group(1)
    if name_match:
        data["name"] = name_match.group(1).strip()
    
    return data
