import sys
import cv2 as cv
import math

def main():
    # 引数: 画像ファイル名, ガンマ値
    if len(sys.argv) != 3:
        print("Usage: python kadai2a.py <image_path> <gamma>")
        sys.exit(1)

    img_path = sys.argv[1]
    try:
        gamma = float(sys.argv[2])
        if gamma <= 0.0:
            raise ValueError
    except ValueError:
        print("Error: gamma must be a positive number.")
        sys.exit(1)

    # 1. 画像を読み込む（グレースケール1ch）
    img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: failed to read image: {img_path}")
        sys.exit(1)

    h, w = img.shape
    inv_gamma = 1.0 / gamma

    # 2. 全画素を走査し、ガンマ変換を適用して上書き
    for y in range(h):
        for x in range(w):
            val = int(img[y, x])
            # [TODO]
            img[y, x] = val

    # 3. 出力
    if not cv.imwrite("output.png", img):
        print("Error: failed to write output.png")
        sys.exit(1)
    print("Saved: output.png")

if __name__ == "__main__":
    main()
