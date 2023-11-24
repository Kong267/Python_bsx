import cv2
import numpy as np
import pytesseract

# Load imgae, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('image/img_8.png')
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9,9), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU)[1]

# Morph close
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# Find contours and filter for QR code
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    x,y,w,h = cv2.boundingRect(approx)
    area = cv2.contourArea(c)
    ar = w / float(h)
    if (len(approx) == 4) and area > 1000 and (ar > .85 and ar < 1.3):
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
        ROI = original[y:y+h, x:x+w]

        gray1 = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        # blur1 = cv2.GaussianBlur(gray1, (9, 9), 0)
        thresh1 = cv2.threshold(gray1, 150, 255, cv2.THRESH_BINARY)[1]



        cv2.imshow(str(x), thresh1)

        # cnts1 = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # cnts1 = cnts1[0] if len(cnts1) == 2 else cnts1[1]
        # print(cnts1)
        # for c1 in cnts1:
        #     # cv2.rectangle(thresh, (x, y), (x + w, y + h), (36, 255, 12), 3)
        #     cv2.drawContours(thresh, cnts1, c1, (0, 255, 0), 2)
        #
        #     ROI1 = original[y:y + h, x:x + w]
        #     cv2.imshow(str(x), thresh)


        # thresh = cv2.threshold(ROI, 0, 255, cv2.THRESH_OTSU)[1]
        # cv2.imshow('output/ROI.png', gray)

        import pytesseract

        # Đọc ảnh
        # image = cv2.imread("output/ROI.png")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # Nhận dạng chữ
        text = pytesseract.image_to_string(gray1)

        print(text)


# cv2.imshow('thresh', thresh)
# cv2.imshow('close', close)
# cv2.imshow('image', image)



# In kết quả
# print(text)

# if(ROI):
#     cv2.imshow('ROI', ROI)
cv2.waitKey()