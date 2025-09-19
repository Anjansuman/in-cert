import re

def extract_certificate_data(words):
    """Map extracted words into structured certificate fields."""
    text_content = " ".join([w['text'] for w in words])
    
    patterns = {
        "name": r"Name[:\-]?\s*([A-Za-z\s]+)",
        "dob": r"Date of Birth[:\-]?\s*([\d\-\/]+)",
        "roll": r"Roll\s*No[:\-]?\s*([A-Za-z0-9]+)",
        "degree": r"(Bachelor|Master|Diploma|Certificate)[A-Za-z\s]*",
    }
    
    extracted = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text_content, re.IGNORECASE)
        if match:
            extracted[field] = match.group(1).strip()
    
    return extracted
