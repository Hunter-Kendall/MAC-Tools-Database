import cv2
from pyzbar import pyzbar

class Scan(object):
    def __init__(self):
        self.outputnum = 0
        self.output = []
    def read_barcodes(self, frame):
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y , w, h = barcode.rect
            barcode_text = barcode.data.decode('utf-8')
            if len(barcode_text) > 1:
                print(barcode_text)
                self.outputnum = self.outputnum + 1
                self.output.append(barcode_text)
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        return frame

    def main(self):
        self.output = []
        self.outputnum = 0
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()

        while self.outputnum < 5:
            ret, frame = camera.read()
            #print(output)
            frame = self.read_barcodes(frame)
            cv2.imshow('Barcode reader', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        result = False
        if len(self.output) > 0:
            result = all(elem == self.output[0] for elem in self.output)

        if result:
            print("Final Output:", self.output[0])
            camera.release()
            cv2.destroyAllWindows()
            return self.output[0]
        else:
            self.output = []
            self.outputnum = 0
            camera.release()
            cv2.destroyAllWindows()
            return None
