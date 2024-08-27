import os
import cv2
from PIL import Image
import pytesseract

class TextExtractor:
    def __init__(self, tesseract_path=None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def _resize_image(self, img, max_size=800):
        height, width = img.shape[:2]
        scale = max_size / max(height, width)
        new_size = (int(width * scale), int(height * scale))
        return cv2.resize(img, new_size)

    def _preprocess_image(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        return morph

    def _find_contours(self, thresh):
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return []

        min_contour_area = 500
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
        return filtered_contours

    def _extract_text_area(self, img, x, y, w, h):
        card = img[y:y + h, x:x + w]
        temp_file = 'temp.jpg'
        cv2.imwrite(temp_file, card)
        r = Image.open(temp_file)
        text = pytesseract.image_to_string(r)
        os.remove(temp_file)
        return text

    def process_image(self, file_path):
        try:
            img = cv2.imread(file_path)
            if img is None:
                print("Error: Unable to read image file.")
                return

            img_resized = self._resize_image(img)
            thresh = self._preprocess_image(img_resized)
            contours = self._find_contours(thresh)

            if not contours:
                print("No significant text areas found.")
                return

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(img_resized, (x, y), (x + w, y + h), (0, 255, 255), 2)
                text = self._extract_text_area(img_resized, x, y, w, h)
                print(f"Extracted text from box ({x}, {y}, {w}, {h}):")
                print(text)

            cv2.imshow("Detected Regions", img_resized)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"Error: {e}")
            return

# Example usage:
# extractor = TextExtractor(tesseract_path='path/to/tesseract')
# extractor.process_image('path/to/image.jpg')
