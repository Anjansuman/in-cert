import sys

# Import from pipelines folder
from pipelines.preprocessing import load_certificate
from pipelines.ocr_module import ocr_with_boxes
from pipelines.alignment_analysis import analyze_text_alignment, check_label_value_alignment
from pipelines.layout_analysis import analyze_layout_structure, compute_layout_metrics
from pipelines.data_extraction import extract_certificate_data
from pipelines.font_quality import check_font_consistency, analyze_text_quality
from pipelines.ela_analysis import ela_features
from pipelines.metadata_check import check_metadata_consistency
from pipelines.scoring import calculate_score


def process_document(file_path):
    """Process a single certificate and return extracted features + score"""
    # Load document
    image, text = load_certificate(file_path)

    # OCR
    ocr_words, ocr_data = ocr_with_boxes(image)

    # Layout + Alignment
    layout_info = analyze_layout_structure(ocr_data)
    alignment_issues = analyze_text_alignment(ocr_data)
    label_value_alignment = check_label_value_alignment(ocr_data)

    # Text/Data extraction
    extracted_data = extract_certificate_data(text)

    # Font/Quality
    font_consistency = check_font_consistency(ocr_data)
    text_quality = analyze_text_quality(image)

    # Forgery detection
    ela_result = ela_features(image)
    metadata_result = check_metadata_consistency(file_path)

    # Score
    score = calculate_score(
        layout_info,
        alignment_issues,
        font_consistency,
        ela_result,
        metadata_result
    )

    return {
        "ocr_words": ocr_words,
        "layout": layout_info,
        "alignment": alignment_issues,
        "label_value_alignment": label_value_alignment,
        "data": extracted_data,
        "font_consistency": font_consistency,
        "text_quality": text_quality,
        "ela_result": ela_result,
        "metadata_result": metadata_result,
        "final_score": score
    }


def jaccard_similarity(text1, text2):
    """Simple OCR text similarity"""
    set1, set2 = set(text1.lower().split()), set(text2.lower().split())
    if not set1 or not set2:
        return 0
    return len(set1 & set2) / len(set1 | set2)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <test_document> <reference_document>")
        sys.exit(1)

    test_file = sys.argv[1]
    reference_file = sys.argv[2]

    # Process both documents
    test_results = process_document(test_file)
    reference_results = process_document(reference_file)

    # Compare OCR text similarity
    test_text = " ".join(test_results["ocr_words"])
    ref_text = " ".join(reference_results["ocr_words"])
    ocr_similarity = jaccard_similarity(test_text, ref_text) * 100

    # Combine into a final authenticity score
    final_auth_score = round(
        0.75 * test_results["final_score"] + 0.25 * ocr_similarity, 2
    )

    # --- Report ---
    print("\n===== CERTIFICATE AUTHENTICITY REPORT =====\n")
    print(f"Test File: {test_file}")
    print(f"Reference File: {reference_file}\n")

    print(f"Base Pipeline Score: {test_results['final_score']} / 100")
    print(f"OCR Text Similarity: {ocr_similarity:.2f}%")
    print(f"Final Authenticity Score: {final_auth_score} / 100\n")

    if final_auth_score >= 60:
        print("Likely Authentic")
    else:
        print("Likely Forged / Tampered")


    ## Example run:
    ## python main.py components/test/wbjee_forged.pdf components/forged/WBJEE_RESULT.pdf
