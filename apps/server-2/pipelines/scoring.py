def calculate_score(layout, alignment, font, ela, metadata):
    """
    Combine results into a confidence score.
    """
    score = 100
    score -= alignment["alignment_deviation"] * 0.1
    score -= font["font_stddev"] * 0.05
    score -= ela["ela_mean"] * 0.01
    return max(0, min(100, score))
