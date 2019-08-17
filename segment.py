from sklearn.cluster import DBSCAN
import cv2
import imutils
import numpy as np


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
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title, 600, 600)
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

    eq = equalize_histogram_color(img)
    gray = cv2.cvtColor(eq, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, ddepth=-1)
    blur = cv2.GaussianBlur(lap, (5, 5), 0)

    v = np.median(gray)
    sigma = 0.33

    # ---- apply optimal Canny edge detection using the computed median----
    lower_thresh = int(max(0, (1.0 - sigma) * v))
    upper_thresh = int(min(255, (1.0 + sigma) * v))
    edges = cv2.Canny(blur, lower_thresh, upper_thresh)

    return edges


def equalize_histogram_color(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img


img = cv2.imread("Images/11.jpeg")
edges = get_canny(img)
display_image("Image", img)
display_image("Canny Edges", edges)

num_contours = 999
result = edges.copy()

while(num_contours > 5):
    contours, hierarchy = cv2.findContours(result.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out = np.zeros_like(img)

    result = cv2.drawContours(out, contours, -1, (0, 255, 0), 5)
    result = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
    display_image("Contours", result)
    num_contours = len(contours)

result = cv2.drawContours(img, contours, -1, (0, 255, 0), 5)
display_image("Contours", result)
