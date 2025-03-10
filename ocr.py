from PIL import Image
import pyocr
import cv2
from pathlib import Path


def read_string_decimal(image_path, is_include_plus=False, is_include_dot=False):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        return

    if isinstance(image_path, Path):
        image_path = str(image_path)
    tool = tools[0]
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    custom_whitelist = "0123456789"
    if is_include_plus:
        custom_whitelist += "+"
    if is_include_dot:
        custom_whitelist += "."

    # TextBuilder を使用し、tesseract_configs でホワイトリストを設定
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    builder.tesseract_configs.append(f"tessedit_char_whitelist={custom_whitelist}")
    builder.tesseract_configs.append("tessedit_char_blacklist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ][")

    return tool.image_to_string(image, lang="eng", builder=builder)


def read_eng_string(image_path):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        return
    if isinstance(image_path, Path):
        image_path = str(image_path)
    tool = tools[0]
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    return tool.image_to_string(image, lang="eng", builder=builder)


def crop_image(image_path, new_image_path, x, y, width, height):
    image = cv2.imread(str(image_path))
    image = image[y:y + height, x:x + width]
    cv2.imwrite(str(new_image_path), image)


if __name__ == "__main__":
    BASE_PATH = Path(__file__).parent
    IMAGE_PATH = Path(BASE_PATH, "crop_image_test", "test.png")
    CROP_IMAGE_PATH = Path(BASE_PATH, "crop_image_test", "crop_test.png")
    # Gemの数
    # crop_image(IMAGE_PATH, CROP_IMAGE_PATH, 660, 35, 150, 70)
    # Pre_stage_bonus
    # crop_image(IMAGE_PATH, CROP_IMAGE_PATH, 660, 2000, 200, 70)
    print(read_string_decimal(CROP_IMAGE_PATH, is_include_plus=True, is_include_dot=True))
    print(read_string_decimal(CROP_IMAGE_PATH, is_include_plus=False, is_include_dot=False))
