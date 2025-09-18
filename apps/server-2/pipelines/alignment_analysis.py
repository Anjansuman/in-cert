def analyze_text_alignment(ocr_data):
    """
    Check if text alignment is consistent.
    """
    avg_left = ocr_data['left'].mean()
    alignment_issues = (ocr_data['left'] - avg_left).abs().mean()
    return {"alignment_deviation": alignment_issues}

def check_label_value_alignment(ocr_data):
    """
    Dummy placeholder – check spacing between labels and values.
    """
    return {"label_value_mismatch": False}
