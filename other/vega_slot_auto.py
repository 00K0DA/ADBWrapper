from ADBWrapper import ADBWrapper
from time import sleep
from MyLogger import MyLogger

adb = ADBWrapper("25111FDF6001YX")
adb.set_print_flag(False)
logger = MyLogger()


def main():
    count = 0
    while True:
        count += 1
        logger.info("Count: {}".format(count))
        logger.info("Tap Down Button 3 times")
        for _ in range(3):
            tap_down_button()
        sleep(0.5)
        logger.info("Tap A Button 3 times")
        for _ in range(3):
            tap_a_button()

        sleep(2)


def tap_down_button():
    adb.longTap(300, 2050, 0)


def tap_a_button():
    adb.longTap(765, 1755, 0, end_time=0.5)


if __name__ == "__main__":
    main()
