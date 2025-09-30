#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 使い方例:
# python to_gray_resize_save.py --img 入力画像.png --out 出力画像.png

import argparse
import numpy as np
import cv2

def imread_unicode(path):
    """日本語パス対応で画像を読む"""
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_UNCHANGED)

def imwrite_unicode(path, img, ext=".png"):
    """日本語パス対応で画像を書き出す"""
    import os
    _, ext_from_path = os.path.splitext(path)
    if ext_from_path:
        ext = ext_from_path
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        raise IOError("画像のエンコードに失敗しました")
    buf.tofile(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="画像をグレースケール化し、640x480以内に等比縮小して保存")
    parser.add_argument("--img", required=True, help="入力画像のパス")
    parser.add_argument("--out", required=True, help="出力画像のパス（例: out.png, out.jpg など）")
    args = parser.parse_args()

    # 読み込み
    src = imread_unicode(args.img)
    if src is None:
        raise FileNotFoundError(f"画像を読み込めませんでした: {args.img}")

    # 必ず1ch（グレー）へ
    if src.ndim == 2:
        gray = src  # 既に1ch
    else:
        # BGR(3ch) / BGRA(4ch) を想定
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # 640x480以内に、アスペクト比を保って縮小（必要なときだけ）
    h, w = gray.shape[:2]
    max_w, max_h = 640, 480

    # 縮小率（拡大はしないため1.0で頭打ち）
    scale_w = max_w / w
    scale_h = max_h / h
    scale = min(scale_w, scale_h, 1.0)

    if scale < 1.0:
        new_w = max(1, int(round(w * scale)))
        new_h = max(1, int(round(h * scale)))
        # 縮小時は INTER_AREA が無難
        gray = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # 保存
    imwrite_unicode(args.out, gray)
    print(f"Saved grayscale (<=640x480, keep aspect) image to: {args.out}")
