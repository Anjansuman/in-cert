# final test 2

import os
import cv2
import pytesseract
import numpy as np
import pdfplumber
from PIL import Image, ImageChops, ImageEnhance
import re
from collections import Counter

# -------- STEP 1: Handle PDF/Image Upload --------
def load_certificate(file_path):
    """Load PDF or image. For PDF, return extracted words with bounding boxes."""
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            first_page = pdf.pages[0]
            
            # Try to extract words directly
            words = first_page.extract_words()
            if words:  
                extracted = []
                for w in words:
                    extracted.append({
                        'text': w['text'],
                        'conf': 99.0,  # pdfplumber doesn't provide confidence
                        'bbox': (int(w['x0']), int(w['top']),
                                 int(w['x1'] - w['x0']), int(w['bottom'] - w['top']))
                    })
                return extracted, None  # return words directly
            
            # If no text layer (scanned), fallback to OCR
            img = first_page.to_image(resolution=300).original
            img_path = file_path.replace(".pdf", "_page.png")
            img.save(img_path)
            return None, img_path
    else:
        return None, file_path

# -------- STEP 2: OCR with bounding boxes (only if scanned) --------
def ocr_with_boxes(image_path):
    """Perform OCR on an image and return words with bounding boxes."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    words = []
    for i, txt in enumerate(data['text']):
        if txt.strip():
            words.append({
                'text': txt.strip(),
                'conf': float(data['conf'][i]),
                'bbox': (data['left'][i], data['top'][i],
                         data['width'][i], data['height'][i])
            })
    return words

# -------- STEP 3: Extract structured certificate details --------
def extract_certificate_data(words):
    """Map extracted words into structured certificate fields."""
    text_content = " ".join([w['text'] for w in words])
    
    # Example regex patterns for typical fields
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

# -------- STEP 4: Compare alignment between reference & test --------
def compare_alignment(ref_words, test_words, tolerance=10):
    """Compare positions of key fields between reference and test certificates."""
    forged_areas = []
    
    ref_map = {w['text'].lower(): w['bbox'] for w in ref_words}
    test_map = {w['text'].lower(): w['bbox'] for w in test_words}
    
    for word, ref_bbox in ref_map.items():
        if word in test_map:
            test_bbox = test_map[word]
            dx = abs(ref_bbox[0] - test_bbox[0])
            dy = abs(ref_bbox[1] - test_bbox[1])
            if dx > tolerance or dy > tolerance:
                forged_areas.append((word, ref_bbox, test_bbox))
    return forged_areas

# -------- STEP 5: Main analysis function --------
def analyze_certificate(test_file, reference_file=None):
    """Analyze a certificate for potential forgery."""
    try:
        
        test_words, test_img_path = load_certificate(test_file)
        if test_words is None:  
            test_words = ocr_with_boxes(test_img_path)
        
        test_cert_data = extract_certificate_data(test_words)

        forged_areas = []
        ref_cert_data = {}
        
        if reference_file:
            ref_words, ref_img_path = load_certificate(reference_file)
            if ref_words is None:
                ref_words = ocr_with_boxes(ref_img_path)
            ref_cert_data = extract_certificate_data(ref_words)
            
            # Alignment comparison
            forged_areas = compare_alignment(ref_words, test_words)
        
        # Compute validity score
        score = 100
        issues = []
        if forged_areas:
            score -= len(forged_areas) * 20
            issues.append("Misaligned fields detected (possible forgery).")
        
        return {
            "status": "success",
            "validity_score": max(score, 0),
            "issues": issues,
            "extracted_data": test_cert_data,
            "forged_areas": forged_areas
        }
    
    except Exception as e:
        return {
            "status": "error",
            "validity_score": 0,
            "issues": [f"Error during analysis: {str(e)}"]
        }

# -------- Example usage --------
if __name__ == "__main__":
    test_pdf = "components/original/praroop_wbjee.pdf"
    ref_pdf = "components/original/WBJEE_RESULT.pdf"
    
    result = analyze_certificate(test_pdf, ref_pdf)
    print("Status:", result["status"])
    print("Validity Score:", result["validity_score"])
    print("Issues Found:", result["issues"])
    print("Extracted Data:", result["extracted_data"])
    if result["forged_areas"]:
        print("Forged Areas (word, ref_bbox, test_bbox):", result["forged_areas"])