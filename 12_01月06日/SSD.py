import cv2

# 1. 画像の読み込み（2枚とも，グレースケール指定）
base_img = cv2.imread("baseimage.png", cv2.IMREAD_GRAYSCALE)
temp_img = cv2.imread("template.png", cv2.IMREAD_GRAYSCALE)

# 2. baseimage.pngをラスタスキャン（2重for文），ストライド5px（5pxずつズラす）
base_h, base_w = base_img.shape[:2]
temp_h, temp_w = temp_img.shape[:2]
print("base_img サイズ：", base_w, base_h)
print("temp_img サイズ：", temp_w, temp_h)

min_x = 0
min_y = 0
min_v = 9999999
for base_x in range(0,base_w-temp_w,5):
  for base_y in range(0,base_h-temp_h,5):

    # テンプレート画像のサイズで切り出す
    base_img_crop = base_img[base_y:base_y+temp_w, base_x:base_x+temp_h]

    # 2.1 SSDの計算① 2重for文で，各画素の引き算の2乗
    sum = 0
    for temp_x in range(0,temp_w,1):
      for temp_y in range(0,temp_h,1):

        # 2.2 SSDの計算② 総和を求める
        sum += \
          (int(temp_img[temp_y, temp_x]) - int(base_img_crop[temp_y, temp_x])) * \
          (int(temp_img[temp_y, temp_x]) - int(base_img_crop[temp_y, temp_x]))

    # 2.3 SSDで計算したものの，最も小さい値の時の，画像上のインデックスを保持する
    if sum < min_v:
      min_v = sum
      min_x = base_x
      min_y = base_y

# 3. 2.3で求まった，インデックスの場所に矩形を描画
cv2.rectangle(base_img, (min_x, min_y),  (min_x+temp_w, min_y+temp_h), 255, thickness=1, lineType=cv2.LINE_8, shift=0)

# 4. 「output.png」というファイル名で保存する
cv2.imwrite("output.png", base_img)