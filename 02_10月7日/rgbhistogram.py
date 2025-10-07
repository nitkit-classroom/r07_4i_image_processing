# rgb_histogram.py
# 使い方:
#   python rgb_histogram.py input.jpg          # 画面に表示のみ
#   python rgb_histogram.py input.jpg out.png  # ヒストグラム画像を保存
#   ※ ヒストグラム数値は rgb_histogram.csv に保存されます

import sys
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# ----- 引数の確認 -----
if len(sys.argv) < 2:
    print("使い方: python rgb_histogram.py 入力画像 [出力画像]")
    sys.exit(1)

in_path = sys.argv[1]
out_path = sys.argv[2] if len(sys.argv) >= 3 else None

# ----- 画像読み込み（BGR -> RGBへ変換） -----
img_bgr = cv2.imread(in_path, cv2.IMREAD_COLOR)
if img_bgr is None:
    print("画像を読み込めませんでした: ", in_path)
    sys.exit(1)

img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# ----- ヒストグラム計算（各チャンネル256ビン、0～255） -----
# 上から下へ順に処理（関数化しない）
r = img_rgb[:, :, 0].ravel()
g = img_rgb[:, :, 1].ravel()
b = img_rgb[:, :, 2].ravel()

bins = np.arange(257)  # 0..256（区切り）
hist_r, _ = np.histogram(r, bins=bins, range=(0, 256))
hist_g, _ = np.histogram(g, bins=bins, range=(0, 256))
hist_b, _ = np.histogram(b, bins=bins, range=(0, 256))

# ----- CSVに保存（列: value, R, G, B） -----
values = np.arange(256)  # 0..255
csv_data = np.column_stack([values, hist_r, hist_g, hist_b])
header = "value,R,G,B"
np.savetxt("rgb_histogram.csv", csv_data, fmt="%d", delimiter=",", header=header, comments="")
print("ヒストグラム値を保存しました: rgb_histogram.csv")

# ----- ヒストグラム描画 -----
plt.figure(figsize=(8, 4.5), dpi=120)
plt.plot(values, hist_r, label="R", linewidth=1)
plt.plot(values, hist_g, label="G", linewidth=1)
plt.plot(values, hist_b, label="B", linewidth=1)
plt.xlim(0, 255)
plt.xlabel("Pixel value")
plt.ylabel("Count")
plt.title(f"RGB Histogram: {os.path.basename(in_path)}")
plt.legend()
plt.tight_layout()

# 保存指定があれば保存、なければ表示
if out_path is not None:
    plt.savefig(out_path)
    print("ヒストグラム画像を保存しました:", out_path)
else:
    plt.show()

