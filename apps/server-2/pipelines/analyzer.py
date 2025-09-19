from pipelines.preprocessing import load_certificate
from pipelines.ocr_module import ocr_with_boxes
from pipelines.data_extraction import extract_certificate_data
from pipelines.alignment_analysis import compare_alignment
from pipelines.scoring import compute_score

def analyze_certificate(test_file, reference_file=None):
    try:
        # Process test file
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
            forged_areas = compare_alignment(ref_words, test_words)

        # Score
        score, issues = compute_score(forged_areas)

        return {
            "status": "success",
            "validity_score": score,
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
