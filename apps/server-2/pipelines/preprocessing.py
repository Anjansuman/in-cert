import os
from pdf2image import convert_from_path
from PIL import Image

def load_certificate(file_path):
    """
    Load PDF or image and return (PIL image, extracted text if PDF else "").
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        images = convert_from_path(file_path)
        return images[0], ""  # for now, no PDF text
    elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
        return Image.open(file_path), ""
    else:
        raise ValueError(f"Unsupported file format: {ext}")
