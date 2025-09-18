from PIL import Image, ImageChops, ImageEnhance
import numpy as np

def ela_features(image, quality=90):
    """
    Error Level Analysis for forgery detection.
    """
    temp_filename = "temp_ela.jpg"
    image.save(temp_filename, 'JPEG', quality=quality)
    compressed = Image.open(temp_filename)

    ela_image = ImageChops.difference(image, compressed)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])

    scale = 255.0 / max_diff if max_diff != 0 else 1
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

    mean_val = np.array(ela_image).mean()
    return {"ela_mean": mean_val}
