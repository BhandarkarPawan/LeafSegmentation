import cv2
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from matplotlib import cm


def mouse_callback(event, x, y, flags, param):
    global marks_updated

    if event == cv2.EVENT_LBUTTONDOWN:

        # TRACKING FOR MARKERS
        cv2.circle(marker_image, (x, y), 10, (current_marker), -1)

        # DISPLAY ON USER IMAGE
        cv2.circle(img_copy, (x, y), 10, colors[current_marker], -1)
        marks_updated = True


def detect_leaf(img):
    # This method returns the green part of the image
    l_b = np.array([30, 0, 60])
    u_b = np.array([255, 255, 255])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, l_b, u_b)

    res = cv2.bitwise_and(img, img, mask=mask)

    return res


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


def nothing(x):
    pass


def check_HLS(img):
    '''
    Creates a tracker with adjustable sliders for the H, L and S
    values of an image. Use this function to find the boundaries of HSL
    values which can be used as the mask for color based segmentation
    '''

    cv2.namedWindow("Tracker")
    cv2.createTrackbar("LH", "Tracker", 0, 255, nothing)
    cv2.createTrackbar("UH", "Tracker", 255, 255, nothing)
    cv2.createTrackbar("LL", "Tracker", 0, 255, nothing)
    cv2.createTrackbar("UL", "Tracker", 255, 255, nothing)
    cv2.createTrackbar("LS", "Tracker", 0, 255, nothing)
    cv2.createTrackbar("US", "Tracker", 255, 255, nothing)

    while True:
        # Convert to HLS Color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

        l_h = cv2.getTrackbarPos("LH", "Tracker")
        l_l = cv2.getTrackbarPos("LL", "Tracker")
        l_s = cv2.getTrackbarPos("LS", "Tracker")

        u_h = cv2.getTrackbarPos("UH", "Tracker")
        u_l = cv2.getTrackbarPos("UL", "Tracker")
        u_s = cv2.getTrackbarPos("US", "Tracker")

        # Get the values from the sliders
        l_b = np.array([l_h, l_l, l_s])
        u_b = np.array([u_h, u_l, u_s])

        # Generate masks
        mask = cv2.inRange(hsv, l_b, u_b)

        res = cv2.bitwise_and(hsv, hsv, mask=mask)
        res2 = cv2.bitwise_and(img, img, mask=mask)

        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', 600, 600)
        cv2.imshow("image", res2)

        cv2.namedWindow('Mask', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Mask', 600, 600)
        cv2.imshow("Mask", mask)

        cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Result', 600, 600)
        cv2.imshow("Result", res)

        key = cv2.waitKey(1)
        if key == 27:
            break

    # cap.release()
    cv2.destroyAllWindows()


def get_canny(img):

    v = np.median(img)
    sigma = 0.33

    # ---- apply optimal Canny edge detection using the computed median----
    lower_thresh = int(max(0, (1.0 - sigma) * v))
    upper_thresh = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(img, lower_thresh, upper_thresh)

    return edges


def equalize_histogram_color(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img


def get_contour(img, num_contours=999):
    edges = get_canny(img)
    result = edges.copy()

    while(num_contours > 5):
        contours, hierarchy = cv2.findContours(
            result.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        out = np.zeros_like(img)

        result = cv2.drawContours(out, contours, -1, (0, 255, 0), 5)
        result = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
        display_image("Contours", result)
        num_contours = len(contours)

    result = cv2.drawContours(img, contours, -1, (0, 255, 0), 5)
    display_image("Contours", result)


def create_rgb(i):
    x = np.array(cm.tab10(i))[:3]*255
    return tuple(x)


'''================================Test Area================================'''
OnePlus = glob('./Images/OnePlus 7/*')
Xiaomi = glob('./Images/Xiaomi Note 3/*')


img = cv2.imread(OnePlus[5])
img = cv2.resize(img, (img.shape[1]//5, img.shape[0]//5))
# display_image("Image " + str(img.shape), img)


eq = equalize_histogram_color(img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# display_image("Gray ", gray)

blur = cv2.GaussianBlur(gray, (7, 7), 0)
lap = cv2.Laplacian(blur, ddepth=-1)
# display_image("LoG", lap)

edges = get_canny(blur)
# display_image("Edges", edges)


'''
=================WaterShed Starts here========================== '''
img_copy = np.copy(eq)
colors = []
n_markers = 10

# One color for each single digit
for i in range(10):
    colors.append(create_rgb(i))
current_marker = 1
marks_updated = False
segments = np.zeros(img.shape, dtype=np.uint8)
marker_image = np.zeros(img.shape[:2], dtype=np.int32)

cv2.namedWindow('Road Image')
cv2.setMouseCallback('Road Image', mouse_callback)

while True:

    # SHow the 2 windows
    cv2.imshow('WaterShed Segments', segments)
    cv2.imshow('Road Image', img_copy)

    #
    k = cv2.waitKey(1)

    # Close everything if Esc is pressed
    if k == 27:
        break

    # Clear all colors and start over if 'c' is pressed
    elif k == ord('c'):
        img_copy = img.copy()
        marker_image = np.zeros(img.shape[0:2], dtype=np.int32)
        segments = np.zeros(img.shape, dtype=np.uint8)

    # If a number 0-9 is chosen index the color
    elif k > 0 and chr(k).isdigit():
        current_marker = int(chr(k))
    if marks_updated:

        marker_image_copy = marker_image.copy()
        cv2.watershed(img, marker_image_copy)

        segments = np.zeros(img.shape, dtype=np.uint8)
        for color_ind in range(n_markers):
            segments[marker_image_copy == (color_ind)] = colors[color_ind]

        marks_updated = False

cv2.destroyAllWindows()
