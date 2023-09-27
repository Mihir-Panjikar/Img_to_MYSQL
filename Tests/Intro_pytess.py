import pytesseract
from PIL import Image

img_file = "samples/plain-text.png"

no_noise = "samples/no_noise.png"

with Image.open(img_file) as img:
    ocr_result = pytesseract.image_to_string(img)
    print(ocr_result)