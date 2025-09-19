def compute_score(forged_areas):
    """Compute validity score based on detected issues."""
    score = 100
    issues = []
    if forged_areas:
        score -= len(forged_areas) * 20
        issues.append("Misaligned fields detected (possible forgery).")
    return max(score, 0), issues
