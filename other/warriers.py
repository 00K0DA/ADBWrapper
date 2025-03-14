from ADBWrapper import ADBWrapper
from MyLogger import MyLogger


def main():
    adb = ADBWrapper("25111FDF6001YX")
    adb.set_print_flag(False)
    logger = MyLogger()

    while True:
        logger.info("Tap update tab")
        adb.tap(340, 2240, end_time=1)

        # Tap update food production
        logger.info("Tap update food production")
        adb.tap(900, 1280, end_time=1)

        # Tap Battle tab
        logger.info("Tap Battle tab")
        adb.tap(500, 2240, end_time=1)

        # Start Battle
        logger.info("Start Battle")
        adb.tap(560, 1650, end_time=1)

        # Spwan characters
        logger.info("Spawn characters")
        adb.tap(685, 2035, count=20, span=1, end_time=1)

        # Close battle result
        logger.info("Close battle result")
        adb.tap(565, 1665, count=1, span=1, end_time=1)


if __name__ == "__main__":
    main()
