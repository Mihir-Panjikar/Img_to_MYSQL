import pytesseract
import cv2

image = cv2.imread("Main/Test_1.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (7,7), 0)

kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))

thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

dilate = cv2.dilate(thresh, kernal, iterations=1)

cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if len(cnts) == 2 else cnts[1]

cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

ocr_result = ""
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)        
    roi = image[y:y+h, x:x+w]    
    ocr_result = pytesseract.image_to_string(roi)

cv2.imwrite("Main/Test_1_process.png", image)

print(ocr_result)

# ocr_result = ocr_result.replace("|", "")



# table_data = [[]]

# for row in ocr_result:
#     for column in row:    
#         table_data[[].append()]








# results = []
# for c in cnts:
#     x, y, w, h = cv2.boundingRect(c)
#     if h > 200 and w > 20:
#         cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)
#         ocr_result = ocr_result.split("\n")
#         for item in ocr_result:
#             results.append(item)


# entities = []
# for item in results:
#     item = item.strip().replace("\n", "")
#     item = item.split(" ")[0]
#     if len(item) > 2:
#         if item[0].isupper() or item.lower() and ")" not in item and "‘" not in item[0]:
#             item = item.split(".")[0].replace(":", "")
#             entities.append(item)

# entities = sorted(list(set(entities)))

# for entity in entities:
#     print(entity)

# cv2.imwrite("index_samples/Cnames_bbox_2.jpeg", image)