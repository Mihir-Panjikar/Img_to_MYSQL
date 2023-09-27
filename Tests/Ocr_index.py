import pytesseract
from PIL import Image

image_file = "index_samples/sample_1.png"

with Image.open(image_file) as img:
    ocr_result = pytesseract.image_to_string(img)
    print(ocr_result)