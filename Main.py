import pytesseract
import PIL.Image
import cv2 as cv

myconfig = r"--psm 4"

text = pytesseract.image_to_string(PIL.Image.open(r"C:\Users\rybot\OneDrive\Desktop\Taxes for Code\111\Image Versions\Image 111 S Corp Tax Return IS no Statements.jpg"), config=myconfig)
print(text)

