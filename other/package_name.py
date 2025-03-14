from ADBWrapper import ADBWrapper


def main():
    adb = ADBWrapper("HQ631V0CEF")
    print(adb.getPackageAndActivity())
    adb.launch_app("mobi.ban_ap.banban", "mobi.ban_ap.banban.MainActivity")

if __name__ == "__main__":
    main()
