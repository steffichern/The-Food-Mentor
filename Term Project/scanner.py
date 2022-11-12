
import cv2
from pyzbar import pyzbar
import requests


def getBarcodes(self, image): # find the barcodes in the image
    allBarcodes = pyzbar.decode(image)  # returns an array of detected barcode
    for barcode in allBarcodes: # loop thru all the barcode detected
        x, y, width, height = barcode.rect  # top left coordinate + rectangle's width + height, contains bounding box of the polygon
        cv2.rectangle(image, (x, y),(x + width, y + height), (0, 255, 0), 3) # rect color (BGR), width, draws the rect
        self.scanUPC = barcode.data.decode('utf-8') # the barcode data is a bytes object, convert to string
        if self.scanUPC[0] == '0':
            self.scanUPC = self.scanUPC.replace('0', '', 1) # remove the first extra 0 at front when scanning
        barcodeType = barcode.type
        textOnBarcode = "{} ({})".format(self.scanUPC, barcodeType)  # draw text on image
        cv2.putText(image, textOnBarcode, (x, y - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (156, 232, 45), 3)
        print('start scanning...')
        print(self.scanUPC)   # string
        #cv2.circle(image, (300,200),100, (255,0,0), 3)
    return image

def runBarcode(self):  # opens the camera
    captureDevice = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # captureDevice = camera
    while True:
        ___, image = captureDevice.read()
        image = getBarcodes(self, image)
        cv2.imshow('Read Barcode', image)
        if cv2.waitKey(1) & 0xFF == ord('e') or self.scanUPC != '':  # waits to prevent freeze for videos, for key event
            print('done scanning! :)')
            break

    captureDevice.release()
    cv2.destroyAllWindows()

    

# reference: https://www.youtube.com/watch?v=bd_eBkQ29rA&ab_channel=KalebuJordan