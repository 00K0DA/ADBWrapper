from ADBWrapper import ADBWrapper
from pathlib import Path


def main():
    file_name_prefix = "牛島さん"
    base_path = Path(__file__).parent
    save_path = Path(base_path, "screenshots")
    if not save_path.exists():
        save_path.mkdir()

    adb = ADBWrapper("RF8MB1TVE3P")

    for i in range(200):
        file_name = "{}_{}".format(file_name_prefix, str(i).zfill(3))
        adb.get_screen_shot(save_path, file_name)
        adb.swipe(300, 1100, 300, 200, end_time=4)


if __name__ == "__main__":
    main()
