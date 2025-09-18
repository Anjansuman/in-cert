def check_font_consistency(ocr_data):
    """
    Check if font sizes vary too much.
    """
    font_heights = ocr_data['height']
    return {"font_stddev": font_heights.std()}

def analyze_text_quality(image):
    """
    Placeholder – blur detection using variance of Laplacian.
    """
    import cv2
    import numpy as np
    
    img_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    variance = cv2.Laplacian(img_gray, cv2.CV_64F).var()
    return {"sharpness_score": variance}
