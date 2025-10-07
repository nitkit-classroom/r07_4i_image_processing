# program2b1.py
# 使い方: python program2b1.py <入力画像> <出力csv>
# 例    : python program2b1.py sample.png hsv.csv
#
# 仕様:
# - RGB画像をHSB(=HSV)に変換しCSVへ保存
# - 保存形態は「1行=画像の1行」、各画素は H,S,B の順で3列を占める
# - 走査順は「右上の画素」から開始し、各行は 右→左、行は 上→下
# - Hは[0,360]度、SとBは[0,100]% (小数第2位まで)

import sys
import csv
import cv2
import numpy as np

def rgb_to_hsv_hsb_degrees_percent(r, g, b):
    """
    OpenCVはBGRなので、呼び出し側でRGBに直してから渡すこと。
    返却: (H[0..360], S[%], B[%])
    """
    # 0..255 -> 0..1 に正規化
    rf = r / 255.0
    gf = g / 255.0
    bf = b / 255.0

    # colorsys を使わず自前で計算（高速化のため配列向け実装でも良いが、シンプルに個別変換）
    cmax = max(rf, gf, bf)
    cmin = min(rf, gf, bf)
    delta = cmax - cmin

    # Hue
    if delta == 0:
        h = 0.0
    elif cmax == rf:
        h = (60 * ((gf - bf) / delta) + 360) % 360
    elif cmax == gf:
        h = (60 * ((bf - rf) / delta) + 120) % 360
    else:  # cmax == bf
        h = (60 * ((rf - gf) / delta) + 240) % 360

    # Saturation (HSVのS)
    s = 0.0 if cmax == 0 else (delta / cmax)

    # Brightness (HSVのV)
    v = cmax

    # %表記へ
    return (h, s * 100.0, v * 100.0)

def main():
    if len(sys.argv) != 3:
        print("Usage: python program2b1.py <input_image> <output_csv>")
        sys.exit(1)

    in_path = sys.argv[1]
    out_csv = sys.argv[2]

    # 画像読み込み (BGR)
    img = cv2.imread(in_path, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Error: failed to read image: {in_path}")
        sys.exit(1)

    h_img, w_img = img.shape[:2]

    # CSV書き出し
    # 1行=画像の1行（上→下）、各行は右→左で画素を走査し、画素ごとに H,S,B を並べる
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # ヘッダ（任意）：右上の画素H/S/B, 1つ右(=右→左走査なので実質「1つ左」) ... のイメージ
        # ※授業・自動採点等で不要なら、このヘッダ行を削除してください。
        header = []
        for x_from_right in range(w_img):
            header.extend([f"H(x={w_img-1 - x_from_right})", f"S(x={w_img-1 - x_from_right})", f"B(x={w_img-1 - x_from_right})"])
        writer.writerow(header)

        for y in range(h_img):            # 上(0) -> 下(h-1)
            row_vals = []
            for x in range(w_img-1, -1, -1):   # 右(w-1) -> 左(0)
                b, g, r = img[y, x]            # OpenCVはBGR
                H, S, Bv = rgb_to_hsv_hsb_degrees_percent(int(r), int(g), int(b))
                # 小数2桁に丸め（必要に応じて変更可）
                row_vals.extend([f"{H:.2f}", f"{S:.2f}", f"{Bv:.2f}"])
            writer.writerow(row_vals)

    print(f"Saved: {out_csv}")
    print(f"Size: {w_img} x {h_img} (W x H) | Order: top->down rows, right->left within each row | Columns per pixel: H,S,B")

if __name__ == "__main__":
    main()

