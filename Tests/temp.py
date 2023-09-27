import pytesseract
import cv2
from table_ocr.extract_cells import extract_cell_images_from_table

# Load the image
image = cv2.imread("Main/Test_1.png")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blur = cv2.GaussianBlur(gray, (7, 7), 0)

# Define a kernel for morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# Threshold the image to create a binary image
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Dilate the thresholded image to close gaps in the table lines
dilate = cv2.dilate(thresh, kernel, iterations=1)

# Extract cells from the dilated image
cells = extract_cell_images_from_table(dilate)

# Now, you can perform OCR on each cell using pytesseract
for cell in cells:
    x, y, w, h = cell
    cell_image = dilate[y:y+h, x:x+w]
    text = pytesseract.image_to_string(cell_image, config='--psm 6')  # Adjust psm mode as needed
    print(f"Cell Text: {text}")

# Optionally, you can visualize the cells by drawing rectangles around them
for cell in cells:
    x, y, w, h = cell
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display or save the image with cell boundaries
cv2.imshow("Image with Cell Boundaries", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
