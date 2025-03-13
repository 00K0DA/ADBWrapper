import cv2
import numpy as np


def is_include_color(x, y, width, height, color, image_path):
    image = cv2.imread(str(image_path))
    image = image[y:y + height, x:x + width]
    # 色をBGRに変換
    color_bgr = (color[2], color[1], color[0])
    return np.any(np.all(image == color_bgr, axis=-1))


def count_color(x, y, width, height, image_path):
    image = cv2.imread(str(image_path))
    image = image[y:y + height, x:x + width]
    color_set = set()
    for row in image:
        for pixel in row:
            color_set.add(tuple(pixel))

    return len(color_set)


def get_color(x, y, image_path):
    image = cv2.imread(str(image_path))
    return image[y, x]
