# demo2 with allignment check

import os
import cv2
import pytesseract
import numpy as np
from pdf2image import convert_from_path
from PIL import Image, ImageChops, ImageEnhance
import re
from collections import Counter

# -------- STEP 1: Handle PDF/Image Upload --------
def load_certificate(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        pages = convert_from_path(file_path, dpi=300)
        image_path = file_path.replace(".pdf", "_page.png")
        pages[0].save(image_path, "PNG")
        return image_path
    else:
        return file_path

# -------- STEP 2: OCR with bounding boxes --------
def ocr_with_boxes(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    words = []
    for i, txt in enumerate(data['text']):
        if txt.strip():
            words.append({
                'text': txt.strip(),
                'conf': float(data['conf'][i]),
                'bbox': (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            })
    return words, data

# -------- STEP 3: Advanced Alignment Analysis --------
def analyze_text_alignment(words, tolerance=5):
    """Comprehensive text alignment analysis"""
    alignment_issues = []
    
    # Group words by approximate Y positions (lines)
    lines = {}
    for word in words:
        if word['conf'] < 50:  # Skip low confidence words
            continue
        y_pos = word['bbox'][1]  # top position
        
        # Find existing line with similar Y position
        matched_line = None
        for line_y in lines.keys():
            if abs(y_pos - line_y) <= tolerance * 2:  # Allow some tolerance for same line
                matched_line = line_y
                break
        
        if matched_line:
            lines[matched_line].append(word)
        else:
            lines[y_pos] = [word]
    
    # Analyze each line for alignment issues
    for line_y, line_words in lines.items():
        if len(line_words) < 2:
            continue
        
        # Sort words by X position
        line_words.sort(key=lambda w: w['bbox'][0])
        
        # Check for unusual gaps between words
        for i in range(len(line_words) - 1):
            current_word = line_words[i]
            next_word = line_words[i + 1]
            
            # Calculate gap between words
            current_right = current_word['bbox'][0] + current_word['bbox'][2]
            next_left = next_word['bbox'][0]
            gap = next_left - current_right
            
            # Check for abnormally large gaps (might indicate inserted text)
            if gap > 50:  # Threshold for suspicious gaps
                alignment_issues.append({
                    'type': 'large_gap',
                    'position': (line_y, current_right),
                    'gap_size': gap,
                    'between': f"'{current_word['text']}' and '{next_word['text']}'"
                })
            
            # Check for overlapping text (negative gap)
            elif gap < -5:
                alignment_issues.append({
                    'type': 'text_overlap',
                    'position': (line_y, current_right),
                    'overlap': abs(gap),
                    'between': f"'{current_word['text']}' and '{next_word['text']}'"
                })
        
        # Check vertical alignment within the line
        y_positions = [w['bbox'][1] for w in line_words]
        if len(set(y_positions)) > 1:  # Multiple Y positions in same line
            y_variance = np.var(y_positions)
            if y_variance > tolerance * tolerance:
                alignment_issues.append({
                    'type': 'vertical_misalignment',
                    'position': line_y,
                    'variance': y_variance,
                    'words': [w['text'] for w in line_words]
                })
    
    return alignment_issues

def check_label_value_alignment(words, tolerance=8):
    """Check alignment between labels and their corresponding values"""
    label_patterns = [
        'Name', 'Roll Number', 'Date of Birth', 'Application No',
        'Gender', 'Category', 'Total', 'Merit rank'
    ]
    
    misalignments = []
    
    for i, word in enumerate(words):
        if word['conf'] < 60:
            continue
            
        # Check if current word is a label
        for pattern in label_patterns:
            if pattern.lower() in word['text'].lower():
                # Look for the next significant word (the value)
                for j in range(i + 1, min(i + 5, len(words))):  # Check next few words
                    next_word = words[j]
                    if next_word['conf'] < 50 or len(next_word['text'].strip()) < 2:
                        continue
                    
                    # Check if they're on the same line (similar Y position)
                    y_diff = abs(word['bbox'][1] - next_word['bbox'][1])
                    if y_diff <= tolerance:
                        # Check horizontal alignment
                        label_right = word['bbox'][0] + word['bbox'][2]
                        value_left = next_word['bbox'][0]
                        gap = value_left - label_right
                        
                        # Flag unusual gaps
                        if gap < 5:  # Too close
                            misalignments.append({
                                'label': word['text'],
                                'value': next_word['text'],
                                'issue': 'too_close',
                                'gap': gap
                            })
                        elif gap > 100:  # Too far
                            misalignments.append({
                                'label': word['text'],
                                'value': next_word['text'],
                                'issue': 'too_far',
                                'gap': gap
                            })
                        break
                    else:
                        # Values should be on the same line as labels
                        if y_diff > tolerance * 2:
                            misalignments.append({
                                'label': word['text'],
                                'value': next_word['text'] if j < len(words) else 'N/A',
                                'issue': 'vertical_misalignment',
                                'y_diff': y_diff
                            })
                        break
                break
    
    return misalignments

# -------- STEP 4: Layout Structure Analysis --------
def analyze_layout_structure(words, image_path):
    """Analyze the overall layout structure for inconsistencies"""
    if not words:
        return {}
    
    # Get image dimensions
    img = cv2.imread(image_path)
    img_height, img_width = img.shape[:2]
    
    # Analyze margins and spacing
    x_positions = [w['bbox'][0] for w in words if w['conf'] > 50]
    y_positions = [w['bbox'][1] for w in words if w['conf'] > 50]
    
    if not x_positions or not y_positions:
        return {}
    
    # Calculate margins
    left_margin = min(x_positions)
    right_margin = img_width - max([w['bbox'][0] + w['bbox'][2] for w in words if w['conf'] > 50])
    top_margin = min(y_positions)
    bottom_margin = img_height - max([w['bbox'][1] + w['bbox'][3] for w in words if w['conf'] > 50])
    
    # Analyze text distribution
    text_width = img_width - left_margin - right_margin
    text_height = img_height - top_margin - bottom_margin
    
    # Find common X positions (column alignment)
    x_rounded = [round(x / 10) * 10 for x in x_positions]  # Round to nearest 10
    common_x_positions = [x for x, count in Counter(x_rounded).most_common(5)]
    
    # Find common Y positions (row alignment)
    y_rounded = [round(y / 5) * 5 for y in y_positions]  # Round to nearest 5
    common_y_positions = [y for y, count in Counter(y_rounded).most_common(10)]
    
    return {
        'margins': {
            'left': left_margin,
            'right': right_margin,
            'top': top_margin,
            'bottom': bottom_margin
        },
        'text_area': {
            'width': text_width,
            'height': text_height
        },
        'common_x_positions': common_x_positions,
        'common_y_positions': common_y_positions,
        'x_position_variance': np.var(x_positions),
        'y_position_variance': np.var(y_positions)
    }

# -------- STEP 5: Extract structured data with position info --------
def extract_certificate_data(words):
    """Extract key information from certificate with position tracking"""
    text = " ".join([w['text'] for w in words])
    
    data = {
        'name': None,
        'roll_number': None,
        'application_no': None,
        'date_of_birth': None,
        'total_score': None,
        'merit_rank_engineering': None,
        'merit_rank_pharmacy': None,
        'downloading_date': None
    }
    
    # Extract with position tracking
    word_dict = {w['text'].lower(): w for w in words}
    
    # Find fields by looking for labels and nearby values
    for word in words:
        text_lower = word['text'].lower()
        
        # Name extraction
        if 'name' in text_lower and not data['name']:
            # Look for capitalized text nearby
            for w in words:
                if (abs(w['bbox'][1] - word['bbox'][1]) <= 10 and  # Same line
                    w['bbox'][0] > word['bbox'][0] and  # To the right
                    w['text'].isupper() and len(w['text']) > 2):
                    data['name'] = w['text']
                    break
    
    # Extract other fields using regex on full text
    name_match = re.search(r'Name\s+([A-Z\s]+?)(?:Roll|$)', text)
    if name_match:
        data['name'] = name_match.group(1).strip()
    
    roll_match = re.search(r'Roll Number\s+(\d+)', text)
    if roll_match:
        data['roll_number'] = roll_match.group(1)
    
    app_match = re.search(r'Application No\s+(\d+)', text)
    if app_match:
        data['application_no'] = app_match.group(1)
    
    dob_match = re.search(r'Date of Birth\s+(\d{2}-\d{2}-\d{4})', text)
    if dob_match:
        data['date_of_birth'] = dob_match.group(1)
    
    total_match = re.search(r'Total\s*:\s*([\d.]+)', text)
    if total_match:
        data['total_score'] = float(total_match.group(1))
    
    merit_eng_match = re.search(r'Merit rank.*?(\d+)\s+(\d+)', text)
    if merit_eng_match:
        data['merit_rank_engineering'] = int(merit_eng_match.group(1))
        data['merit_rank_pharmacy'] = int(merit_eng_match.group(2))
    
    download_match = re.search(r'Downloading Date:\s*(.+?)(?:\s|$)', text)
    if download_match:
        data['downloading_date'] = download_match.group(1).strip()
    
    return data

# -------- STEP 4: Font consistency check --------
def check_font_consistency(words, tolerance=15):
    """Check for unusual font size variations"""
    heights = [w['bbox'][3] for w in words if w['conf'] > 50]
    if len(heights) < 10:
        return True, "Insufficient text for font analysis"
    
    height_counts = Counter(heights)
    most_common_heights = [h for h, count in height_counts.most_common(3)]
    
    unusual_heights = []
    for w in words:
        if w['conf'] > 50:
            height = w['bbox'][3]
            if not any(abs(height - common_h) <= tolerance for common_h in most_common_heights):
                unusual_heights.append((w['text'], height))
    
    if len(unusual_heights) > len(words) * 0.1:  # More than 10% unusual heights
        return False, f"Inconsistent font sizes detected: {len(unusual_heights)} anomalies"
    
    return True, "Font consistency OK"

# -------- STEP 5: Text quality analysis --------
def analyze_text_quality(words):
    """Analyze OCR confidence and text quality"""
    if not words:
        return {"avg_confidence": 0, "low_conf_ratio": 1.0}
    
    confidences = [w['conf'] for w in words]
    avg_conf = np.mean(confidences)
    low_conf_count = sum(1 for conf in confidences if conf < 60)
    low_conf_ratio = low_conf_count / len(confidences)
    
    return {
        "avg_confidence": avg_conf,
        "low_conf_ratio": low_conf_ratio,
        "total_words": len(words)
    }

# -------- STEP 6: Enhanced ELA analysis --------
def ela_features(image_path, scale=10):
    """Enhanced Error Level Analysis"""
    try:
        original = Image.open(image_path).convert('RGB')
        
        # Test with multiple quality levels
        results = {}
        for quality in [70, 80, 90, 95]:
            import io
            buffer = io.BytesIO()
            original.save(buffer, 'JPEG', quality=quality)
            buffer.seek(0)
            compressed = Image.open(buffer)
            
            diff = ImageChops.difference(original, compressed)
            extrema = diff.getextrema()
            max_diff = max([e[1] for e in extrema]) if extrema else 1
            
            if max_diff > 0:
                factor = 255.0 / max_diff
                enhanced = ImageEnhance.Brightness(diff).enhance(factor * scale / 255.0)
                arr = np.array(enhanced).astype(np.float32)
                
                results[f'q{quality}'] = {
                    'mean': float(arr.mean()),
                    'std': float(arr.std()),
                    'max': float(arr.max())
                }
        
        return results
        
    except Exception as e:
        print(f"ELA analysis failed: {e}")
        return {}

# -------- STEP 7: Metadata inconsistency check --------
def check_metadata_consistency(cert_data):
    """Check for logical inconsistencies in certificate data"""
    issues = []
    
    # Check if application number and roll number are consistent
    if cert_data.get('application_no') and cert_data.get('roll_number'):
        app_no = cert_data['application_no']
        roll_no = cert_data['roll_number']
        
        # Basic format checks for WBJEE
        if not re.match(r'^\d{11}$', app_no):
            issues.append("Invalid application number format")
        
        if not re.match(r'^\d{10}$', roll_no):
            issues.append("Invalid roll number format")
    
    # Check date format consistency
    if cert_data.get('date_of_birth'):
        dob = cert_data['date_of_birth']
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', dob):
            issues.append("Invalid date of birth format")
    
    # Check score and rank correlation (basic sanity check)
    if cert_data.get('total_score') and cert_data.get('merit_rank_engineering'):
        score = cert_data['total_score']
        rank = cert_data['merit_rank_engineering']
        
        # Very basic check - extremely high scores shouldn't have very high ranks
        if score > 180 and rank > 10000:
            issues.append("Score-rank correlation seems suspicious")
        elif score < 30 and rank < 1000:
            issues.append("Low score with high rank - suspicious")
    
    return issues

# -------- STEP 8: Main comparison function --------
def analyze_certificate(test_file, reference_file=None):
    """Analyze a certificate for potential forgery"""
    
    try:
        # Load and process test certificate
        test_img = load_certificate(test_file)
        test_words, test_data = ocr_with_boxes(test_img)
        test_cert_data = extract_certificate_data(test_words)
        
        score = 100
        issues = []
        
        print("Extracted Certificate Data:")
        for key, value in test_cert_data.items():
            if value:
                print(f"  {key}: {value}")
        print()
        
        # 1. Advanced alignment analysis
        alignment_issues = analyze_text_alignment(test_words)
        if alignment_issues:
            alignment_score = min(30, len(alignment_issues) * 8)  # Max 30 points deduction
            score -= alignment_score
            
            for issue in alignment_issues[:3]:  # Report first 3 issues
                if issue['type'] == 'large_gap':
                    issues.append(f"Suspicious text gap ({issue['gap_size']}px) between {issue['between']}")
                elif issue['type'] == 'text_overlap':
                    issues.append(f"Text overlap detected ({issue['overlap']}px) between {issue['between']}")
                elif issue['type'] == 'vertical_misalignment':
                    issues.append(f"Vertical misalignment in line: {', '.join(issue['words'][:3])}")
        
        # 2. Label-value alignment check
        label_misalignments = check_label_value_alignment(test_words)
        if label_misalignments:
            alignment_penalty = min(20, len(label_misalignments) * 6)
            score -= alignment_penalty
            
            for misalign in label_misalignments[:3]:
                if misalign['issue'] == 'too_close':
                    issues.append(f"Label '{misalign['label']}' too close to value '{misalign['value']}' ({misalign['gap']}px)")
                elif misalign['issue'] == 'too_far':
                    issues.append(f"Label '{misalign['label']}' too far from value '{misalign['value']}' ({misalign['gap']}px)")
                elif misalign['issue'] == 'vertical_misalignment':
                    issues.append(f"Vertical misalignment: '{misalign['label']}' and '{misalign['value']}' ({misalign['y_diff']}px)")
        
        # 3. Layout structure analysis
        layout_structure = analyze_layout_structure(test_words, test_img)
        if layout_structure:
            # Check for unusual margins
            margins = layout_structure.get('margins', {})
            if margins:
                left_margin = margins.get('left', 0)
                right_margin = margins.get('right', 0)
                
                # Flag asymmetric margins (could indicate cut-paste)
                if abs(left_margin - right_margin) > 50:
                    score -= 10
                    issues.append(f"Asymmetric margins detected (L:{left_margin}px, R:{right_margin}px)")
                
                # Flag unusually small margins
                if left_margin < 10 or right_margin < 10:
                    score -= 8
                    issues.append("Unusually small margins - possible cropping/editing")
        
        # 4. Font consistency check
        font_ok, font_msg = check_font_consistency(test_words)
        if not font_ok:
            score -= 20
            issues.append(font_msg)
        
        # 5. Text quality analysis
        quality_metrics = analyze_text_quality(test_words)
        if quality_metrics['avg_confidence'] < 70:
            score -= 15
            issues.append(f"Low OCR confidence: {quality_metrics['avg_confidence']:.1f}%")
        
        if quality_metrics['low_conf_ratio'] > 0.3:
            score -= 15
            issues.append(f"High ratio of poorly recognized text: {quality_metrics['low_conf_ratio']:.2f}")
        
        # 6. Metadata consistency check
        metadata_issues = check_metadata_consistency(test_cert_data)
        if metadata_issues:
            score -= 10 * len(metadata_issues)
            issues.extend(metadata_issues)
        
        # 7. ELA analysis
        ela_results = ela_features(test_img)
        if ela_results:
            # Look for suspicious ELA patterns
            q90_mean = ela_results.get('q90', {}).get('mean', 0)
            if q90_mean > 50:  # Threshold for suspicious editing
                score -= 25
                issues.append(f"Suspicious ELA signature detected (mean: {q90_mean:.2f})")
        
        # 8. If reference provided, do comparative alignment analysis
        if reference_file:
            ref_img = load_certificate(reference_file)
            ref_words, ref_data = ocr_with_boxes(ref_img)
            ref_cert_data = extract_certificate_data(ref_words)
            
            # Compare alignment patterns
            ref_alignment_issues = analyze_text_alignment(ref_words)
            ref_label_misalignments = check_label_value_alignment(ref_words)
            
            # If test has significantly more alignment issues than reference
            test_alignment_count = len(alignment_issues) + len(label_misalignments)
            ref_alignment_count = len(ref_alignment_issues) + len(ref_label_misalignments)
            
            if test_alignment_count > ref_alignment_count + 2:  # More than 2 extra issues
                score -= 15
                issues.append(f"More alignment issues than reference ({test_alignment_count} vs {ref_alignment_count})")
            
            # Compare layout structures
            ref_layout_structure = analyze_layout_structure(ref_words, ref_img)
            if layout_structure and ref_layout_structure:
                # Compare margins
                test_margins = layout_structure.get('margins', {})
                ref_margins = ref_layout_structure.get('margins', {})
                
                for margin_type in ['left', 'right', 'top', 'bottom']:
                    test_margin = test_margins.get(margin_type, 0)
                    ref_margin = ref_margins.get(margin_type, 0)
                    
                    if abs(test_margin - ref_margin) > 30:  # Significant difference
                        score -= 8
                        issues.append(f"Layout difference: {margin_type} margin varies by {abs(test_margin - ref_margin)}px from reference")
                        break  # Don't penalize multiple times
                
                # Compare text positioning patterns
                test_x_var = layout_structure.get('x_position_variance', 0)
                ref_x_var = ref_layout_structure.get('x_position_variance', 0)
                
                if test_x_var > ref_x_var * 1.5:  # 50% more variance
                    score -= 12
                    issues.append("Text positioning more inconsistent than reference")
            
            # Compare structural elements
            if test_cert_data.get('total_score') == ref_cert_data.get('total_score'):
                if test_cert_data.get('merit_rank_engineering') == ref_cert_data.get('merit_rank_engineering'):
                    score -= 40
                    issues.append("Identical scores and ranks - possible template reuse")
            
            # Compare layout metrics from original function
            test_layout_old = compute_layout_metrics(test_data)
            ref_layout_old = compute_layout_metrics(ref_data)
            
            if test_layout_old and ref_layout_old:
                height_diff = abs(test_layout_old.get('avg_height', 0) - ref_layout_old.get('avg_height', 0))
                if height_diff > 3:
                    score -= 10
                    issues.append(f"Font size inconsistency: height difference {height_diff:.1f}px from reference")
        
        # 9. Look for copy-paste patterns in names/numbers
        if test_cert_data.get('name'):
            name = test_cert_data['name']
            if len(set(name.split())) != len(name.split()):  # Repeated words in name
                score -= 15
                issues.append("Suspicious name pattern detected")
        
        # Final scoring
        score = max(0, min(100, score))
        
        return {
            "status": "Valid" if score >= 70 else "Forgery Suspected",
            "validity_score": score,
            "issues": issues if issues else ["No significant anomalies detected"],
            "certificate_data": test_cert_data,
            "quality_metrics": quality_metrics,
            "alignment_analysis": {
                "text_alignment_issues": len(alignment_issues),
                "label_value_misalignments": len(label_misalignments),
                "layout_structure": layout_structure
            }
        }
        
    except Exception as e:
        return {
            "status": "Analysis Failed",
            "validity_score": 0,
            "issues": [f"Error during analysis: {str(e)}"],
            "certificate_data": {},
            "quality_metrics": {}
        }

# -------- STEP 9: Layout metrics (kept from original) --------
def compute_layout_metrics(ocr_data):
    heights, tops, lefts = [], [], []
    for i, txt in enumerate(ocr_data['text']):
        if not txt.strip(): continue
        heights.append(ocr_data['height'][i])
        tops.append(ocr_data['top'][i])
        lefts.append(ocr_data['left'][i])
    if not heights:
        return {}
    h_avg = float(np.mean(heights))
    h_std = float(np.std(heights))
    left_var = float(np.var(lefts))
    unique_tops = sorted(set(tops))
    line_spacings = np.diff(unique_tops) if len(unique_tops) > 1 else [0]
    line_space_avg = float(np.mean(line_spacings)) if len(line_spacings) else 0.0
    return {
        'avg_height': h_avg,
        'std_height': h_std,
        'left_variance': left_var,
        'avg_line_spacing': line_space_avg
    }

# -------- Example Usage --------
if __name__ == "__main__":
    # Test with the forged certificate
    test_file = "/content/wbjee_forged.pdf"  
    reference_file = "/content/WBJEE_RESULT.pdf"  
    
    print("===== CERTIFICATE VALIDITY ANALYSIS =====\n")
    
    # Analyze the test certificate
    result = analyze_certificate(test_file, reference_file)
    
    print(f"Status: {result['status']}")
    print(f"Validity Score: {result['validity_score']} / 100")
    print("\nIssues Found:")
    for issue in result['issues']:
        print(f" - {issue}")
    
    print(f"\nText Quality Metrics:")
    if result['quality_metrics']:
        print(f" - Average OCR Confidence: {result['quality_metrics']['avg_confidence']:.1f}%")
        print(f" - Low Confidence Ratio: {result['quality_metrics']['low_conf_ratio']:.2f}")
        print(f" - Total Words Detected: {result['quality_metrics']['total_words']}")