import cv2
import sys

# 引数
path = sys.argv[1] # 画像のパス
per  = sys.argv[2] # パーセンテージ
### [実行コマンド] > python ptile.py test.jpg 10

# 画像の準備編
img1 = cv2.imread(path) # 画像を読み込む
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) # グレースケールに変換する

# ヒストグラムを作成する編
value = [0] * 256 # 0～255までの256のリストを準備．0で初期化

# 全ての画素を順番に確認
h, w = img2.shape
for y in range(h):
    for x in range(w):
        value[ img2[y, x] ] += 1

# パーセンテージから，閾値を決める処理
sum   = 0
total = h * w # 全部の画素の数
th    = 0
for i in range(256):
    sum += value[i]
    if float(sum / total)*100 > per: # ここまで足したものが10%を超えて入れば
        th = i
        break

# 閾値から，画像を2値（0か1か）に置換する処理
for y in range(h):
    for x in range(w):
        if img2[y, x] < th:
            img2[y, x] = 0
        else:
            img2[y, x] = 1

# 画像全体を255倍にする処理の追加（表示用）
for y in range(h):
    for x in range(w):
        img2[y, x] *= 255

# 画像を保存するコードの作成（OpenCV関数使用可能）
cv2.imwrite("output.png", img2)

