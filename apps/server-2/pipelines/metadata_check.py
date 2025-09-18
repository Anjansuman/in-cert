from PyPDF2 import PdfReader

def check_metadata_consistency(file_path):
    if file_path.endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            info = reader.metadata
            return {"metadata": dict(info)}
        except Exception:
            return {"metadata": "Error reading PDF metadata"}
    return {"metadata": "Not applicable"}
