# save as decode_certificate.py
# pip install opencv-python pymupdf pillow numpy pytesseract

import os
import cv2
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
import re

# ---------- USER CONFIG ----------
file_path = r"components\image.png"  # <-- put your file path here

# ---------- PDF to image ----------
def image_from_pdf_page(pdf_path, page_num=0, zoom=3.0):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    mode = "RGB" if pix.n == 3 else "RGBA"
    img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# ---------- QR Decode ----------
def decode_qr_opencv(img):
    detector = cv2.QRCodeDetector()
    try:
        retval, decoded_info, _, _ = detector.detectAndDecodeMulti(img)
        if retval:
            return decoded_info
    except Exception:
        pass
    data, _, _ = detector.detectAndDecode(img)
    if data:
        return [data]
    return []

def to_hex_from_result(data_str):
    b = data_str.encode('utf-8', errors='surrogateescape')
    return b.hex()

# ---------- Text + Name Extraction ----------
def extract_text(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def extract_name_from_text(text):
    match = re.search(r"certify that\s+([A-Za-z\s]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

# ---------- Main ----------
def main():
    if not os.path.exists(file_path):
        print("File not found:", file_path); return

    images = []
    if file_path.lower().endswith(".pdf"):
        doc = fitz.open(file_path)
        for i in range(len(doc)):
            images.append(image_from_pdf_page(file_path, page_num=i, zoom=3.0))
    else:
        img = cv2.imread(file_path)
        if img is None:
            print("Failed to open image:", file_path); return
        images.append(img)

    for page_idx, img in enumerate(images):
        print(f"\n--- Page {page_idx+1} ---")

        # QR decoding
        decoded_list = decode_qr_opencv(img)
        if decoded_list:
            for idx, d in enumerate(decoded_list):
                print(f"\nQR #{idx+1}:")
                print("Decoded (text):", d)
                print("Hex (utf-8):", to_hex_from_result(d))
        else:
            print("No QR codes detected on this page.")

        # Text + Name extraction
        text = extract_text(img)
        name = extract_name_from_text(text)
        print("\nExtracted text snippet:\n", text[:200], "...\n")  # preview
        if name:
            print("Extracted Name:", name)
        else:
            print("Name not found in text.")

if __name__ == "__main__":
    main()