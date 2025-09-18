import pytesseract
import pandas as pd

def ocr_with_boxes(image):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DATAFRAME)
    data = data.dropna().reset_index(drop=True)
    words = list(data['text'])
    return words, data
