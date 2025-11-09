# -*- coding: utf-8 -*-
import sys
import cv2 as cv
import numpy as np

if __name__ == "__main__":

    ########################
    # 1. 元画像を読み込む
    ########################
    try:
        print(sys.argv[1])
    except:
        print("引数にファイル名をして下さい")
    img = cv.imread(sys.argv[1], cv.IMREAD_COLOR)

    ########################
    # 2. 元画像と同サイズの3chな黒い画像を（変数としてプログラム内部に）用意する．
    ########################
    h, w = img.shape[:2]
    out = np.full((h, w, 3), 0, np.uint8) 

    ########################
    # 3. 画像処理する
    ########################
    out1 = None
    out2 = None
    out3 = None
    out4 = None
    out5 = None
    out6 = None

    # 3.1 元画像のx軸に関するループ
    for x in range(w):
        # 3.1.1 元画像のy軸に関するループ
        for y in range(h):

            # 3.1.1.1 ある1画素に対して，変換先の座標を求める．
            # 3.1.1.2 その座標に「ある1画素」のデータをコピーする

            # 拡大処理の記述
            out1 = out.copy()

            # 縮小処理の記述
            out2 = out.copy()

            # 回転処理の記述
            out3 = out.copy()

            # 鏡移処理の記述
            out4 = out.copy()

            # スキュー処理の記述
            out5 = out.copy()

            # 並行移動処理の記述
            out6 = out.copy()

            pass # 処理記述後に削除

    ########################
    # 4. 画像を保存する
    ########################
    cv.imwrite("img1_kakudai.png", out1)
    cv.imwrite("img2_syukusyo.png", out2)
    cv.imwrite("img3_kaiten.png", out3)
    cv.imwrite("img4_kyoei.png", out4)
    cv.imwrite("img5_sukyu.png", out5)
    cv.imwrite("img6_heiko.png", out6)
    print("DONE")
