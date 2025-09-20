from fastapi import FastAPI, UploadFile, File
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile

# Import your ML pipeline
from pipelines.analyzer import analyze_certificate

# Initialize FastAPI app
app = FastAPI(title="Certificate Forgery Detection API")

# Add CORS middleware to allow requests from your frontend
# This is crucial for the HTML file to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict this for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_class=PlainTextResponse)
async def analyze(
    test_file: UploadFile = File(...),
    reference_file: UploadFile = File(...)
):
    """
    Endpoint to analyze a test certificate against a reference certificate.
    Returns a clean text report instead of raw JSON.
    """
    # Save uploaded files temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(test_file.filename)[1]) as tmp_test:
        tmp_test.write(await test_file.read())
        test_path = tmp_test.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(reference_file.filename)[1]) as tmp_ref:
        tmp_ref.write(await reference_file.read())
        ref_path = tmp_ref.name

    # --- CORRECTED LOGIC ---
    # Run the ML pipeline once with both files for comparison
    results = analyze_certificate(test_path, ref_path)

    # Generate human-readable report from the single result
    report_lines = [
        "===== CERTIFICATE ANALYSIS REPORT =====\n",
        f"Test File: {test_file.filename}",
        f"Reference File: {reference_file.filename}\n",
        f"🔹 Validity Score: {results.get('validity_score', 'N/A')} / 100\n",
        "===== Detailed Analysis ====="
    ]
    
    # Add issues found, if any
    issues = results.get("issues", [])
    if issues:
        report_lines.append("Issues Found:")
        for issue in issues:
            report_lines.append(f"- {issue}")
    else:
        report_lines.append("No major issues found.")
    
    report_lines.append("\n===== Extracted Data (from Test Certificate) =====")
    extracted_data = results.get("extracted_data", {})
    if extracted_data:
        for key, val in extracted_data.items():
            report_lines.append(f"{key.replace('_', ' ').title()}: {val}")
    else:
        report_lines.append("Could not extract data.")

    forged_areas = results.get("forged_areas", [])
    if forged_areas:
        report_lines.append("\n===== Potential Forged Areas =====")
        report_lines.append(f"Found {len(forged_areas)} areas with potential misalignment.")
        # You can add more details about the forged areas here if needed
        # for area in forged_areas:
        #     report_lines.append(str(area))


    # Clean up temporary files
    os.remove(test_path)
    os.remove(ref_path)

    return "\n".join(report_lines)

# To run this app, save the code and use the command:
# uvicorn backend:app --reload

