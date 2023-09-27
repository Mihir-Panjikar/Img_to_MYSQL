import pytesseract
import cv2

# image = cv2.imread("index_samples/sample_1.png")
image = cv2.imread("index_samples/Cnames.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# cv2.imwrite("index_samples/sample_1_gray.png", gray)

blur = cv2.GaussianBlur(gray, (7,7), 0)

# cv2.imwrite("index_samples/sample_1_blur.png", blur)

thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# cv2.imwrite("index_samples/sample_1_thresh.png", thresh)

kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))

dilate = cv2.dilate(thresh, kernal, iterations=1)

# cv2.imwrite("index_samples/sample_1_dilated.png", dilate)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if len(cnts) == 2 else cnts[1]

cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

# for c in cnts:
#     x, y, w, h = cv2.boundingRect(c)
#     cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)

# cv2.imwrite("index_samples/sample_1_bbox.png", image)

results = []
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h > 200 and w > 20:
        roi = image[y:y+h, x:x+h]
        cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)
        ocr_result = pytesseract.image_to_string(roi)
        ocr_result = ocr_result.split("\n")
        for item in ocr_result:
            results.append(item)


entities = []
for item in results:
    item = item.strip().replace("\n", "")
    item = item.split(" ")[0]
    if len(item) > 2:
        if item[0].isupper() or item.lower() and ")" not in item and "‘" not in item[0]:
            item = item.split(".")[0].replace(":", "")
            entities.append(item)
            
entities = sorted(list(set(entities)))

for entity in entities:
    print(entity)

# cv2.imwrite("index_samples/Cnames_bbox_2.jpeg", image)