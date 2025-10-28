import sys
import cv2 as cv
import numpy as np

if __name__ == "__main__":

    #=== 設定：半径の大きさ ===
    r = 0.5
    #==========================

    img = cv.imread(sys.argv[1], cv.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"cannot read: {sys.argv[1]}")

    h, w = img.shape
    cy, cx = h // 2, w // 2
    radius = int(r * min(h, w) / 2.0)

    yy, xx = np.ogrid[:h, :w]
    circle = ((yy - cy) ** 2 + (xx - cx) ** 2) <= (radius ** 2)
    circle = circle.astype(np.uint8)*255
    cv.imwrite("output_circle.png", circle)