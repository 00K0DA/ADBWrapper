import cv2
import numpy as np


def is_include_color(x, y, width, height, color, image_path):
    image = cv2.imread(str(image_path))
    image = image[y:y + height, x:x + width]
    # 色をBGRに変換
    color_bgr = (color[2], color[1], color[0])
    return np.any(np.all(image == color_bgr, axis=-1))
