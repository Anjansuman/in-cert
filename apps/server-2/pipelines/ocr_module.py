import cv2
import pytesseract

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
