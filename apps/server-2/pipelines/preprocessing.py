import os
import pdfplumber

def load_certificate(file_path):
    """Load PDF or image. For PDF, return extracted words with bounding boxes."""
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            first_page = pdf.pages[0]
            words = first_page.extract_words()
            if words:
                extracted = []
                for w in words:
                    extracted.append({
                        'text': w['text'],
                        'conf': 99.0,
                        'bbox': (int(w['x0']), int(w['top']),
                                 int(w['x1'] - w['x0']), int(w['bottom'] - w['top']))
                    })
                return extracted, None
            img = first_page.to_image(resolution=300).original
            img_path = file_path.replace(".pdf", "_page.png")
            img.save(img_path)
            return None, img_path
    else:
        return None, file_path
