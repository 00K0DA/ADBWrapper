from PIL import Image
import cv2
import numpy as np
from pathlib import Path

from machigai.domain.Coordinate import Coordinate

BASE_PATH = Path(__file__).parent


def main(image_path: Path):
    image = cv2.imread(str(image_path))

    (first_start_x, first_start_y, first_end_x, first_end_y) = get_image_coordinates(
        image_path=image_path,
        start_y=300,
        end_y=1750
    )
    print(first_start_x, first_start_y, first_end_x, first_end_y)
    (second_start_x, second_start_y, second_end_x, second_end_y) = get_image_coordinates(
        image_path=image_path,
        start_y=first_end_y + 1,
        end_y=2000
    )
    print(second_start_x, second_start_y, second_end_x, second_end_y)

    first_image = image[first_start_y:first_end_y, first_start_x:first_end_x]
    second_image = image[second_start_y:second_end_y, second_start_x:second_end_x]

    diff_coordinate_list = create_diff_image(first_image, second_image)

    tap_coordinate_list = []
    # ここで画像全体での座標に変換している
    for x, y, w, h in diff_coordinate_list:
        tap_x = x + first_start_x + w // 2
        tap_y = y + first_start_y + h // 2
        tap_coordinate_list.append((tap_x, tap_y))

    return tap_coordinate_list


def get_diff_coordinates(image_path: Path, first_image_coordinate: Coordinate, second_image_coordinate: Coordinate):
    image = cv2.imread(str(image_path))
    first_image = image[first_image_coordinate.start_y:first_image_coordinate.end_y,
                  first_image_coordinate.start_x:first_image_coordinate.end_x]
    second_image = image[second_image_coordinate.start_y:second_image_coordinate.end_y,
                   second_image_coordinate.start_x:second_image_coordinate.end_x]
    diff_coordinate_list = create_diff_image(first_image, second_image)

    tap_coordinate_list = []
    # ここで画像全体での座標に変換している
    for x, y, w, h in diff_coordinate_list:
        tap_x = x + first_image_coordinate.start_x + w // 2
        tap_y = y + first_image_coordinate.start_y + h // 2
        tap_coordinate_list.append((tap_x, tap_y))
    return tap_coordinate_list


def create_diff_image(first_image, second_image):
    # 1. 1枚目と2枚目の画像の差分を取得
    diff = cv2.absdiff(first_image, second_image)

    # 2. グレースケールに変換
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # 3. 閾値処理（二値化）
    _, binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

    # 4. ノイズ除去（膨張・収縮処理）
    kernel = np.ones((10, 10), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)  # 小さな穴を埋める

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    diff_coordinates_list = []
    # 座標を取得
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # 面積が一定以下の場合はノイズとみなして無視する
        if cv2.contourArea(contour) < 20:
            continue
        diff_coordinates_list.append((x, y, w, h))
        cv2.rectangle(first_image, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # for contour in contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     if cv2.contourArea(contour) < 10:
    #         continue
    #     diff_coordinates_list.append((x, y, w, h))
    #     cv2.rectangle(first_image, (x, y), (x + w, y + h), (0, 255, 0), 3)
    #
    # show_image(first_image)

    return diff_coordinates_list


def get_image_coordinates(image_path: Path, start_y: int, end_y: int):
    image = cv2.imread(str(image_path))
    image = image[start_y:end_y, :]
    background_color = image[0, 0]
    image_width = image.shape[1]
    x = image_width // 2

    image_start_y = 0
    # 縦が背景から画像になる境界を探す
    for y in range(0, image.shape[0]):
        if not np.all(image[y, x] == background_color):
            image_start_y = y
            break

    # 縦が画像から背景になる境界を探す
    image_end_y = image_start_y
    for y in range(image_start_y, image.shape[0]):
        if np.all(image[y, 500] == background_color):
            image_end_y = y
            break

    y = (image_start_y + image_end_y) // 2

    # 横が背景から画像になる境界を探す
    image_start_x = 0
    for x in range(0, image_width):
        if not np.all(image[y, x] == background_color):
            image_start_x = x
            break

    # 横が画像から背景になる境界を探す
    image_end_x = image_start_x
    for x in range(image_start_x, image_width):
        if np.all(image[y, x] == background_color):
            image_end_x = x
            break

    return image_start_x, image_start_y + start_y, image_end_x, image_end_y + start_y


def show_image(image):
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main("")
