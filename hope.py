import cv2
from glob import glob
from segment import display_image
import numpy as np


from segment import check_HLS


def display_image(title, image):
    # Function to display an image. Close window using ESC key
    # cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    # cv2.resizeWindow(title, 600, 600)
    cv2.imshow(title, image)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            break
    cv2.destroyAllWindows()


OnePlus = glob('../Images/Good/*')

for i in range(len(OnePlus)):
    img = cv2.imread(OnePlus[i])
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
    R = markers.astype(np.uint8)

    final = cv2.bitwise_and(img, img, mask=R)
    hsv = cv2.cvtColor(final, cv2.COLOR_BGR2HSV)

    l_b = np.array([1, 0, 0])
    u_b = np.array([255, 255, 255])

    # Generate masks
    mask = cv2.inRange(hsv, l_b, u_b)
    total = mask.sum()

    l_b = np.array([1, 0, 0])
    u_b = np.array([30, 255, 255])

    # Generate masks
    mask = cv2.inRange(hsv, l_b, u_b)
    disease = mask.sum()

    display_image("Success!" + str(round(disease/total * 100, 2)) + "%", mask)

    cv2.imwrite("./Image.jpg", R)

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
