import cv2
image_file =  "samples/plain-text.png"

img = cv2.imread(image_file)

invert_img = cv2.bitwise_not(img)
cv2.imwrite("samples/inverted.png", invert_img)