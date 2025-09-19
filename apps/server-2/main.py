from pipelines.analyzer import analyze_certificate

if __name__ == "__main__":
    test_pdf = "components/original/praroop_wbjee.pdf"
    ref_pdf = "components/original/WBJEE_RESULT.pdf"

    result = analyze_certificate(test_pdf, ref_pdf)

    print("Status:", result["status"])
    print("Validity Score:", result["validity_score"])
    print("")
    print("Issues Found:", result["issues"])
    print("")
    print("Extracted Data:", result["extracted_data"])
    print("")
    if result["forged_areas"]:
        print("Forged Areas (word, ref_bbox, test_bbox):", result["forged_areas"])
