import easyocr
import numpy as np
import cv2

class ImageTextExtractor:
    def __init__(self, languages=['en']):
        self.reader = easyocr.Reader(languages)

    def extract_text(self, image_bytes):
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        results = self.reader.readtext(image)
        return [text for (_, text, _) in results]

    def print_text(self, image_path):
        texts = self.extract_text(image_path)
        for text in texts:
            print(text)
