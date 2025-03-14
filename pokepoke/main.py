from ADBWrapper import ADBWrapper


def main():
    adb = ADBWrapper("37311FDJG009F5")
    package_name, activity_name = adb.getPackageAndActivity()
    print(package_name)
    print(activity_name)
    from pathlib import Path
    base_path = Path(__file__).parent
    adb.get_screen_shot(base_path, "home")


if __name__ == "__main__":
    main()
