from PIL import Image

im_file = "samples/plain-text.png"

with Image.open(im_file) as im:
    im = im.rotate(90)
    im.save("samples/rotated.png")