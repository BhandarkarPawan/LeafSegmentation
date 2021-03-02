import numpy as np
from interfaces.segmenter import Segmenter
from typing import Dict
import cv2 

class WaterShedSegmenter(Segmenter):
    def __init__(self):
        super().__init__()

    def process(self,img: np.ndarray) -> np.ndarray:

        scale = 1
        x, y = img.shape[1]//scale, img.shape[0]//scale
        img = cv2.resize(img, (x, y))
        
        dots = np.zeros((y, x))

        Yc, Xc = y//2, x//2
        dx = x//20
        dy = y//20

        for a in range(dx, x-dx):
            dots[y - dy, a] = 2
            dots[dy, a] = 2

        for a in range(dy, y-dy):
            dots[a, dx] = 2
            dots[a, x - dx] = 2

        dots[Yc - dy, Xc] = 1
        dots[Yc, Xc - dx] = 1
        dots[Yc - dy, Xc - dx] = 1
        dots[Yc + dy, Xc] = 1
        dots[Yc, Xc + dx] = 1
        dots[Yc + dy, Xc + dx] = 1
        dots[Yc + dy, Xc - dx] = 1
        dots[Yc - dy, Xc + dx] = 1

        # Apply watershed
        markers = cv2.watershed(img, dots.astype(np.int32))
        markers = (markers + 1)/3.0 * 255
        markers[markers == 255] = 0
        markers[markers > 0] = 255.0
        markers = markers.astype(np.uint8)

        final = cv2.bitwise_and(img, img, mask=markers)

        # Color correction
        final = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)

        print(final.shape)
        return final

    def run(self, image: np.ndarray) -> np.ndarray:
        print("The Segmenter will now run")
        return self.process(image)