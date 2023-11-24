import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = cv2.imread("image/img_9.png")

# # Xác định tỷ lệ thay đổi kích thước
# fx = 0.3
# fy = 0.3
#
# # Thay đổi kích thước hình ảnh
# image = cv2.resize(image, None, fx=fx, fy=fy)

# Chuyển đổi hình ảnh sang chế độ nhị phân
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
cv2.imshow('thresh', gray)

custom_config = r'--oem 3 --psm 6 outputbase digits'


# Đọc biển số xe bằng OCR
text = pytesseract.image_to_string(image, lang='eng')



print( text.replace('|', ''))

cv2.waitKey()