import cv2
import numpy as np
from PIL import Image
import pytesseract
import pyzbar
from pyzbar import pyzbar
import re
# import binascii
import fitz  # PyMuPDF for PDF handling
import os
import io
from pathlib import Path

class CertificateAnalyzer:
    def __init__(self, file_path):
        """
        Initialize the certificate analyzer with the path to the certificate file (image or PDF).
        
        Args:
            file_path (str): Path to the certificate file (supports images and PDFs)
        """
        self.file_path = file_path
        self.image = None
        self.candidate_name = None
        self.jwt_token_hex = None
        self.file_extension = Path(file_path).suffix.lower()
    
    def load_image(self):
        """Load the certificate image from file (supports both images and PDFs)."""
        try:
            if self.file_extension == '.pdf':
                return self._load_from_pdf()
            else:
                return self._load_from_image()
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def _load_from_image(self):
        """Load image from standard image formats (jpg, png, etc.)."""
        self.image = cv2.imread(self.file_path)
        if self.image is None:
            raise ValueError(f"Could not load image from {self.file_path}")
        return True
    
    def _load_from_pdf(self):
        """Load image from PDF file (converts first page to image)."""
        try:
            # Open PDF document
            pdf_document = fitz.open(self.file_path)
            
            # Get first page (assuming certificate is on first page)
            page = pdf_document[0]
            
            # Convert page to image (high resolution for better OCR and QR detection)
            mat = fitz.Matrix(3, 3)  # 3x zoom for better quality
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("ppm")
            pil_image = Image.open(io.BytesIO(img_data))
            
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            self.image = opencv_image
            pdf_document.close()
            return True
            
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def extract_candidate_name(self):
        """
        Extract the candidate name from the certificate using OCR.
        Uses pattern matching similar to your reference code.
        """
        try:
            # Convert image to PIL format for OCR
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            
            # Extract text using OCR
            extracted_text = pytesseract.image_to_string(pil_image)
            print(f"Extracted text: {extracted_text}")
            
            # Name extraction patterns based on your reference code
            name_patterns = [
                r"This is to certify that\s+([A-Za-z\s]+)\s+has",
                r"certify that\s+([A-Za-z\s]+)\s+has",
                r"Name[:\-]?\s*([A-Za-z\s]+)",
                r"awarded to\s+([A-Za-z\s]+)\s+",
                r"presented to\s+([A-Za-z\s]+)\s+",
            ]
            
            # Try each pattern to find the name
            for pattern in name_patterns:
                match = re.search(pattern, extracted_text, re.IGNORECASE)
                if match:
                    name = match.group(1).strip()
                    # Clean up the name (remove extra spaces and common words)
                    name = re.sub(r'\s+', ' ', name)  # Replace multiple spaces with single space
                    self.candidate_name = name
                    print(f"Found candidate name: {self.candidate_name}")
                    return self.candidate_name
            
            print("Could not extract candidate name using standard patterns")
            return None
            
        except Exception as e:
            print(f"Error extracting candidate name: {e}")
            return None
    
    def find_and_decode_qr(self):
        """
        Find and decode QR code from the certificate image.
        Returns the JWT token in hex format.
        """
        try:
            # Convert to grayscale for better QR code detection
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            
            # Try to find QR codes using pyzbar
            qr_codes = pyzbar.decode(gray)
            
            if not qr_codes:
                print("No QR codes found, trying image preprocessing...")
                # Try different preprocessing techniques
                
                # Method 1: Gaussian blur and threshold
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                _, thresh1 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                qr_codes = pyzbar.decode(thresh1)
                
                if not qr_codes:
                    # Method 2: Adaptive threshold
                    thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                   cv2.THRESH_BINARY, 11, 2)
                    qr_codes = pyzbar.decode(thresh2)
                
                if not qr_codes:
                    # Method 3: Morphological operations
                    kernel = np.ones((3,3), np.uint8)
                    morph = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
                    qr_codes = pyzbar.decode(morph)
            
            if qr_codes:
                for qr_code in qr_codes:
                    # Get the raw data from QR code
                    qr_data = qr_code.data
                    
                    if isinstance(qr_data, bytes):
                        # Convert bytes to hex
                        hex_data = binascii.hexlify(qr_data).decode('utf-8')
                    else:
                        # Convert string to bytes first, then to hex
                        hex_data = binascii.hexlify(qr_data.encode('utf-8')).decode('utf-8')
                    
                    self.jwt_token_hex = hex_data
                    print(f"QR Code found and decoded to hex: {hex_data}")
                    return hex_data
            else:
                print("No QR codes could be detected in the image")
                return None
                
        except Exception as e:
            print(f"Error decoding QR code: {e}")
            return None
    
    def analyze_certificate(self):
        """
        Main method to analyze the certificate - extract name and decode QR code.
        
        Returns:
            dict: Dictionary containing candidate name and JWT token in hex format
        """
        results = {
            'candidate_name': None,
            'jwt_token_hex': None,
            'success': False
        }
        
        # Load the image
        if not self.load_image():
            return results
        
        # Extract candidate name
        self.extract_candidate_name()
        results['candidate_name'] = self.candidate_name
        
        # Find and decode QR code
        self.find_and_decode_qr()
        results['jwt_token_hex'] = self.jwt_token_hex
        
        # Check if analysis was successful
        if self.candidate_name or self.jwt_token_hex:
            results['success'] = True
        
        return results

def analyze_certificate_document(file_path):
    """
    Convenience function to analyze a certificate document (image or PDF).
    
    Args:
        file_path (str): Path to the certificate file (image or PDF)
        
    Returns:
        dict: Analysis results containing candidate name and JWT token hex
    """
    analyzer = CertificateAnalyzer(file_path)
    return analyzer.analyze_certificate()

def extract_name_only(image_or_pdf_path):
    """
    Simple function to extract only the candidate name from certificate.
    Based on your reference code pattern.
    
    Args:
        image_or_pdf_path (str): Path to certificate file
        
    Returns:
        str: Extracted candidate name or None if not found
    """
    try:
        analyzer = CertificateAnalyzer(image_or_pdf_path)
        if analyzer.load_image():
            # Convert image to PIL format for OCR
            image_rgb = cv2.cvtColor(analyzer.image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            
            # Extract all text
            text_content = pytesseract.image_to_string(pil_image)
            
            # Name extraction patterns (following your reference style)
            name_patterns = {
                "certify_pattern": r"This is to certify that\s+([A-Za-z\s]+)\s+has",
                "name_field": r"Name[:\-]?\s*([A-Za-z\s]+)",
                "awarded_pattern": r"awarded to\s+([A-Za-z\s]+)",
            }
            
            # Try each pattern
            for pattern_name, pattern in name_patterns.items():
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    name = match.group(1).strip()
                    # Clean up name (remove extra spaces)
                    name = re.sub(r'\s+', ' ', name)
                    print(f"Name found using {pattern_name}: {name}")
                    return name
            
            print("No name found with any pattern")
            return None
            
    except Exception as e:
        print(f"Error extracting name: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Simple name extraction
    certificate_path = "components/image.pdf"
    name = extract_name_only(certificate_path)
    print(f"Extracted Name: {name}")