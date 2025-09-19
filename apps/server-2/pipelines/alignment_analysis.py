def compare_alignment(ref_words, test_words, tolerance=10):
    """Compare positions of key fields between reference and test certificates."""
    forged_areas = []
    ref_map = {w['text'].lower(): w['bbox'] for w in ref_words}
    test_map = {w['text'].lower(): w['bbox'] for w in test_words}
    
    for word, ref_bbox in ref_map.items():
        if word in test_map:
            test_bbox = test_map[word]
            dx = abs(ref_bbox[0] - test_bbox[0])
            dy = abs(ref_bbox[1] - test_bbox[1])
            if dx > tolerance or dy > tolerance:
                forged_areas.append((word, ref_bbox, test_bbox))
    return forged_areas
