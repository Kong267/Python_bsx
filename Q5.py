import sys
import cv2
import pytesseract
import re
import imutils

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QVBoxLayout

class App(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()
    self.filePath = ''
  def initUI(self):
    self.setWindowTitle("Chọn ảnh")
    self.resize(300, 200)

    self.btnOpen = QPushButton("Chọn file")
    self.btnOpen.clicked.connect(self.openFile)

    self.lblPath = QLabel("")
    self.lblImage1 = QLabel("")

    self.detect = QLabel("")
    self.lblImage = QLabel("")

    self.layout = QVBoxLayout()

    self.layout.addWidget(self.btnOpen)

    self.layout.addWidget(self.lblPath)
    self.layout.addWidget(self.lblImage1)

    self.layout.addWidget(self.detect)
    self.layout.addWidget(self.lblImage)

    self.setLayout(self.layout)

  def openFile(self):
    fileName, _ = QFileDialog.getOpenFileName(self, "Mở ảnh", "", "Ảnh (*.jpg *.png *.jpeg)")
    if fileName:
      self.lblPath.setText(fileName)

      pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
      original_image = cv2.imread(fileName)

      self.lblPath.setText(fileName)
      image1 = QPixmap(fileName)

      self.lblImage1.setPixmap(image1)

      original_image = imutils.resize(original_image, width=500)
      gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
      gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)

      edged_image = cv2.Canny(gray_image, 30, 200)

      contours, new = cv2.findContours(edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
      img1 = original_image.copy()
      cv2.drawContours(img1, contours, -1, (0, 255, 0), 3)
      # cv2.imshow("img1", img1)

      contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

      # stores the license plate contour
      screenCnt = None
      img2 = original_image.copy()

      # draws top 30 contours
      cv2.drawContours(img2, contours, -1, (0, 255, 0), 3)
      # cv2.imshow("img2", img2)

      count = 0
      idx = 7

      for c in contours:
        # approximate the license plate contour
        contour_perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * contour_perimeter, True)

        # Look for contours with 4 corners
        if len(approx) == 4:
          screenCnt = approx

          # find the coordinates of the license plate contour
          x, y, w, h = cv2.boundingRect(c)
          new_img = original_image[y: y + h, x: x + w]

          # stores the new image
          cv2.imwrite('./' + str(idx) + '.png', new_img)
          idx += 1
          break

      # draws the license plate contour on original image
      cv2.drawContours(original_image, [screenCnt], -1, (0, 255, 0), 3)
      # cv2.imshow("detected license plate", original_image)

      # filename of the cropped license plate image
      cropped_License_Plate = './7.png'

      img = cv2.imread(cropped_License_Plate)

      # cv2.imshow("cropped license plate", img)

      # converts the license plate characters to string
      text = pytesseract.image_to_string(img, lang='eng', config='--psm 7')

      text = "Biển số xe : " + re.sub(r'[^a-zA-Z0-9.-]', '', text)

      # print("License plate is:", re.sub(r'[^a-zA-Z0-9.-]', '', text))

      image = QPixmap('./7.png')

      self.detect.setText(text)

      self.lblImage.setPixmap(image)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  ex = App()
  ex.show()
  sys.exit(app.exec_())

