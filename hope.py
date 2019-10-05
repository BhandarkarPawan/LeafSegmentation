import cv2
from glob import glob
# from segment import display_image
import numpy as np

OnePlus = glob('./leaves/Images/Xiaomi Note 3/*')

for i in range(len(OnePlus)):
    img = cv2.imread(OnePlus[0])
    x, y = img.shape[1]//5, img.shape[0]//5
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

    # display_image("Dots", dots)

    markers = cv2.watershed(img, dots.astype(int)).get()

    markers = (markers + 1)/3.0 * 255
    markers[markers == 255] = 0
    markers[markers > 0] = 255.0
    cv2.imwrite("./Image.jpg", markers.astype(np.uint8))

    '''
    dots[dy, dx] = 2
    dots[dy, x/2] = 2
    dots[dy, x - dx] = 2
    dots[y - dy, dx] = 2
    dots[y - dy, x/2] = 2
    dots[y - dy, x - dx] = 2
    dots[Yc, x - dx] = 2
    dots[Yc, dx] = 2

    dots[Yc + y/4, dx] = 2
    dots[Yc + y/4, x - dx] = 2
    dots[y/4, dx] = 2
    dots[y/4, x - dx] = 2

    dots[dy, Xc + x/4] = 2
    dots[dy , x/4 ] = 2
    dots[y - dy, Xc + x/4] = 2
    dots[y - dy , x/4 ] = 2
    '''
