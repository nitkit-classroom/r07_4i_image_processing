#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 使い方例:
# python profile_y_loop.py --img lena_gray.png --y_num 120 --graph out_profile.png

import argparse
import numpy as np
import cv2
import matplotlib
matplotlib.use("Agg")  # 画面なし環境OK
import matplotlib.pyplot as plt

def imread_unicode(path):
    # 日本語パス対応の単純な読み込み
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_UNCHANGED)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="指定Yのラインプロファイル（1pxずつ読み出し）")
    parser.add_argument("--img", required=True, help="入力画像のパス（グレー画像想定）")
    parser.add_argument("--y_num", required=True, type=int, help="Y座標（整数）")
    parser.add_argument("--graph", required=True, help="出力グラフ画像のパス（例: out.png）")
    args = parser.parse_args()

    # 画像読み込み（グレー想定）
    img = imread_unicode(args.img)
    if img is None:
        raise FileNotFoundError(f"画像を読み込めませんでした: {args.img}")

    # 念のためカラーならグレーへ
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = img.shape[:2]

    # Y座標を範囲に収める
    y = args.y_num
    if y < 0:
        y = 0
    if y > h - 1:
        y = h - 1

    # 水平ラインを作成
    x_list  = [0] * w
    for x in range(w):
        x_list[x]  = x         # x座標リストも同様に代入

    # --- [TODO] ここを完成させなさい ---
    # (1) 画像の横幅と同じサイズの「空の」リストを用意
    #    （別解: 空で作って append してもOK。ここでは初期化→代入にしています）
    profile = [0] * w

    # (2) 画像から 1px ずつ読み出してリスト（x_list）へ入れる
    #    img[y, x] はその画素の輝度値（0〜255想定）

    # --- [TODO] ここを完成させなさい ---

    # 左: 入力画像+ライン, 右: プロファイル
    fig = plt.figure(figsize=(10, 4), dpi=150)

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(img, cmap="gray", vmin=0, vmax=255)
    ax1.axhline(y, linewidth=1.5)  # 水平ライン（デフォルト色）
    ax1.set_title(f"Input (y={y})")
    ax1.set_axis_off()

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.plot(x_list, profile)  # リストをそのまま描画
    ax2.set_xlim(0, w - 1)
    ax2.set_ylim(0, 255)
    ax2.set_xlabel("x (pixel)")
    ax2.set_ylabel("intensity (0-255)")
    ax2.set_title("Line profile (built by per-pixel loop)")
    ax2.grid(True, linestyle=":", linewidth=0.5)

    fig.tight_layout()
    plt.savefig(args.graph, bbox_inches="tight")
    plt.close(fig)
