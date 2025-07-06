import cv2
import numpy as np
from PIL import Image


from typing import List, Tuple


class ImageProcessor:
    def __init__(self, target_color: Tuple):
        self.target_color = target_color

    def process_image(self, pil_image: Image.Image) -> List[Tuple[float, float]]:
        """Обрабатывает изображение и возвращает центры соответствующих форм"""
        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        # Получение изображения обработки
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        bin_image  = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]

        # Поиск форм на обработанном изображении
        contours = cv2.findContours(bin_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, offset=(0,0))[0]

        # Определение центров форм
        centers = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                center_x = x + w/2
                center_y = y + h/2
                color = pil_image.getpixel((center_x, center_y))
                centers.append((center_x, center_y, area, color))

        return centers