from ADBWrapper import ADBWrapper
from time import sleep


def main():
    adb = ADBWrapper("25111FDF6001YX")
    adb.set_print_flag(False)

    for i in range(200):
        print(i)

        print("update_employee")
        update_employee(adb)
        tap_screen(adb, count=1)

        print("update_speed")
        update_speed(adb)
        tap_screen(adb, count=1)

        print("update_benefit")
        update_benefit(adb)
        tap_screen(adb, count=1)

        if i % 9 == 0:
            print("rebuild")
            rebuild(adb)
            tap_screen(adb, count=1)

            print("get_level_up_reward")
            get_level_up_reward(adb)

        tap_screen(adb, count=10)


def tap_screen(adb: ADBWrapper, count: int = 10):
    for _ in range(count):
        adb.tap(500, 1000, end_time=1)


def update_benefit(adb: ADBWrapper):
    adb.tap(220, 2110, end_time=1)


def update_speed(adb: ADBWrapper):
    adb.tap(520, 2110, end_time=1)


def update_employee(adb: ADBWrapper):
    adb.tap(820, 2110, end_time=1)


def rebuild(adb: ADBWrapper):
    tap_screen(adb, count=2)
    adb.tap(500, 1800, end_time=2, count=2, span=1)
    adb.tap(500, 1700, end_time=8)
    adb.tap(1000, 250, end_time=1)
    adb.tap(1050, 650, end_time=1)
    adb.tap(1030, 145, end_time=1)


def get_level_up_reward(adb: ADBWrapper):
    adb.tap(880, 150, end_time=1)
    adb.tap(1010, 640, end_time=1)
    adb.tap(1030, 145, end_time=1)


if __name__ == "__main__":
    main()
