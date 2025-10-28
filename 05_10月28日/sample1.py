import sys
import cv2 as cv
import numpy as np

def image_to_amplitude(img_gray: np.ndarray):
    """
    入力: 8bitグレー画像
    出力:
      spec_vis ... 表示用の振幅スペクトル画像 (uint8)
      amp       ... シフト後の振幅スペクトル（実数, float32）
      phase     ... シフト後の位相スペクトル（実数, float32, [-pi,pi]）
    """

    # フーリエ変換
    f = np.fft.fft2(img_gray.astype(np.float32))
    fshift = np.fft.fftshift(f)
    amp = np.abs(fshift)
    phase = np.angle(fshift)

    # 振幅スペクトル画像の可視化
    spec_vis = np.log1p(amp)
    spec_vis = cv.normalize(spec_vis, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
    return spec_vis, amp.astype(np.float32), phase.astype(np.float32)

def amplitude_to_output(amp: np.ndarray, phase: np.ndarray):
    """
    入力:
      amp, phase ... image_to_amplitude() が返すシフト後スペクトル
    出力:
      out_img     ... 出力画像 (uint8)
    """

    # ヒント：amp2へ渡すamp画像（振幅スペクトル画像）を
    # 適切にマスク処理すれば良い

    # 逆フーリエ
    amp2 = amp
    fshift_lp = amp2 * np.exp(1j * phase)
    f_ishift = np.fft.ifftshift(fshift_lp)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.real(img_back)

    # 表示・保存用に 0-255 へ正規化
    out_img = cv.normalize(img_back, None, 0, 255, cv.NORM_MINMAX).astype(np.uint8)
    return out_img

if __name__ == "__main__":
    img = cv.imread(sys.argv[1], cv.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"cannot read: {sys.argv[1]}")

    # ① 元画像　→　振幅スペクトル
    spec_vis, amp, phase = image_to_amplitude(img)
    cv.imwrite("spec_out.png", spec_vis)

    # ② 振幅スペクトル　→　出力画像
    out_img = amplitude_to_output(amp, phase)
    cv.imwrite("output1.png", out_img)