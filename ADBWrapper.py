import re
import subprocess
import time
from pathlib import Path
from typing import Union
from threading import Timer
from MyLogger import MyLogger


class ADBWrapper:
    logger = MyLogger("ADBWrapper")
    __DEFAULT_DEVICE_CODE = "__DEFAULT_DEVICE_CODE"
    __COMMAND_TEMPLATE_TAP = "shell input touchscreen tap {x} {y}"
    __COMMAND_TEMPLATE_DOWN = "shell input motionevent DOWN {x} {y}"
    __COMMAND_TEMPLATE_UP = "shell input motionevent UP {x} {y}"
    __COMMAND_TEMPLATE_MOVE = "shell input motionevent MOVE {x} {y}"
    __COMMAND_TEMPLATE_SWIPE = "shell input touchscreen swipe {x1} {y1} {x2} {y2} {swipe_speed}"
    __COMMAND_TEMPLATE_LAUNCH = "shell am start -n {app_id}/{activity_name}"
    __COMMAND_TEMPLATE_TAKE_SCREENSHOT = "shell screencap -p /sdcard/screen_shot_temp.png"
    __COMMAND_TEMPLATE_SYNC = "shell sync"
    __COMMAND_TEMPLATE_PULL_SCREENSHOT = "pull /sdcard/screen_shot_temp.png {path}"
    __COMMAND_TEMPLATE_REMOVE_SCREENSHOT = "shell rm /sdcard/screen_shot_temp.png"
    __COMMAND_TEMPLATE_BROADCAST = "shell am broadcast -a {intent_filter}"
    __COMMAND_TEMPLATE_GET_PACKAGE = "shell dumpsys activity activities"
    __COMMAND_TEMPLATE_CONNECT_WIRELESS = "connect {ip_address}:{port}"
    __COMMAND_TEMPLATE_GET_EVENT = "shell getevent -lt"
    __COMMAND_TEMPLATE_KEY_EVENT = "shell input keyevent {key_code}"
    __COMMAND_REBOOT = "reboot"
    __COMMAND_WAIT_FOR_DEVICE = "wait-for-device"
    __COMMAND_WAIT_FOR_BOOT_COMPLETE = "shell getprop sys.boot_completed"
    __COMMAND_TEMPLATE_STOP_APP = "shell am force-stop {app_id}"
    __COMMAND_TEMPLATE_DISPLAY_DALTONIZER_ENABLED = "shell settings put secure accessibility_display_daltonizer_enabled {enabled}"
    __COMMAND_TEMPLATE_DISPLAY_DALTONIZER_GARY_SCALE = "shell settings put secure accessibility_display_daltonizer 0"
    __COMMAND_PRESS_BACK_BUTTON = "shell input keyevent KEYCODE_BACK"
    __COMMAND_TEMPLATE_INPUT_TEXT = "shell input text {text}"

    def __init__(self, target_device_code: str = __DEFAULT_DEVICE_CODE, print_flag: bool = True):
        self.deviceCode = target_device_code
        self.logger.isPrintLog(print_flag)

    def addLogFilePath(self, path: Path) -> None:
        self.logger.addLogFilePath(path)

    def setPrintFlag(self, print_flag: bool) -> None:
        self.logger.isPrintLog(print_flag)

    def setFileFlag(self, file_flag: bool) -> None:
        self.logger.isPrintLog(file_flag)

    def tap(self, x: int, y: int, sync_flag: bool = True, count: int = 1, span: int = 0,
            end_time: int or float = 0) -> None:
        self.logger.info("Tap x={}, y={}".format(x, y))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_TAP.format(x=x, y=y)
        )
        for _ in range(count):
            if sync_flag:
                subprocess.run(cmdList, stdout=subprocess.DEVNULL)
            else:
                subprocess.Popen(cmdList, stdout=subprocess.DEVNULL)
            if span != 0:
                time.sleep(span)
        if end_time != 0:
            time.sleep(end_time)

    def longTap(self, x: int, y: int, hold_time: int, sync_flag: bool = True, count: int = 1, span: int = 0,
                end_time: int = 0) -> None:
        self.logger.info("LongTap x={}, y={}, holdTime={}".format(x, y, hold_time))
        downCommandList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_DOWN.format(x=x, y=y)
        )
        upCommandList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_UP.format(x=x, y=y)
        )
        for _ in range(count):
            if sync_flag:
                subprocess.run(downCommandList, stdout=subprocess.DEVNULL)
                time.sleep(hold_time)
                subprocess.run(upCommandList, stdout=subprocess.DEVNULL)
            else:
                subprocess.Popen(downCommandList, stdout=subprocess.DEVNULL)
                time.sleep(hold_time)
                subprocess.Popen(upCommandList, stdout=subprocess.DEVNULL)
            if span != 0:
                time.sleep(span)
        if end_time != 0:
            time.sleep(end_time)

    def swipe(self, x1: int, y1: int, x2: int, y2: int, end_time: int or float = 0, swipe_speed: int = 1000) -> None:
        self.logger.info("Swipe x={} to {}, y={} to {}".format(x1, x2, y1, y2))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_SWIPE.format(
                x1=x1, y1=y1, x2=x2, y2=y2, swipe_speed=swipe_speed
            )
        )
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def down(self, x: int, y: int, end_time: int = 0) -> None:
        self.logger.info("DOWN x={}, y={}".format(x, y))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_DOWN.format(x=x, y=y)
        )
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def move(self, x: int, y: int, end_time: int = 0, sync_flag: bool = True) -> None:
        self.logger.info("MOVE x={}, y={}".format(x, y))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_MOVE.format(x=x, y=y)
        )
        if sync_flag:
            subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        else:
            subprocess.Popen(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def up(self, x: int, y: int, end_time: int = 0) -> None:
        self.logger.info("(UP x={}, y={}".format(x, y))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_UP.format(x=x, y=y)
        )
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        if end_time != 0:
            time.sleep(end_time)

    def launchApp(self, app_id: str, activity_name: str) -> None:
        self.logger.info("LaunchApp app_id = {}, activity = {}".format(app_id, activity_name))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_LAUNCH.format(
                app_id=app_id,
                activity_name=activity_name
            )
        )
        subprocess.run(cmdList, stdout=subprocess.PIPE)

    def getScreenShot(self, path: Path, file_name: str) -> None:
        filePath = Path(path, file_name + ".png")
        self.logger.info("ScreenShot = {}".format(filePath))
        while True:
            result = subprocess.run(
                self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_TAKE_SCREENSHOT),
                stdout=subprocess.PIPE
            )
            if result.returncode == 0:
                break
            else:
                time.sleep(1)
        subprocess.run(
            self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_SYNC),
            stdout=subprocess.DEVNULL
        )
        subprocess.run(
            self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_PULL_SCREENSHOT.format(path=filePath)),
            stdout=subprocess.DEVNULL
        )
        subprocess.run(
            self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_REMOVE_SCREENSHOT),
            stdout=subprocess.DEVNULL
        )

    def sendBroadcastCommand(self, intent_filter: str, args: dict[str, Union[str, int]]) -> None:
        self.logger.info("SendBroadcast intent_filter={}".format(intent_filter))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_BROADCAST.format(intent_filter=intent_filter)
        )
        for k, v in args.items():
            if type(v) == str:
                self.logger.info("type=String key={}, value={}".format(k, v))
                cmdList.extend(["--es", str(k), str(v)])
            elif type(v) == int:
                self.logger.info("type=Int key={}, value={}".format(k, v))
                cmdList.extend(["--ei", str(k), str(v)])
        self.logger.info(cmdList)
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def getPackageAndActivity(self) -> tuple[str, str]:
        while True:
            result = subprocess.run(
                self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_GET_PACKAGE),
                stdout=subprocess.PIPE
            )
            if result.returncode == 0:
                break
            else:
                time.sleep(1)

        for string in result.stdout.decode("utf-8").split("\n"):
            if "ResumedActivity: ActivityRecord" in string:
                infoTextList = string.lstrip(" ").split(" ")[3].split("/")
                package = infoTextList[0]
                activity = infoTextList[1]
                self.logger.info("package={}".format(package))
                self.logger.info("activity={}".format(activity))
                return package, activity
        return "", ""

    def wirelessConnect(self, ip_address: str, port: str) -> None:
        self.logger.info("Connect to {}:{}".format(ip_address, port))
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_CONNECT_WIRELESS.format(ip_address=ip_address, port=port)
        )
        self.deviceCode = "{}:{}".format(ip_address, port)
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def pressPowerButton(self) -> None:
        self.logger.info("Press Power Button")
        self.__keyEvent("KEYCODE_POWER")

    def reboot(self) -> None:
        self.logger.info("Reboot")
        cmdList = self.__createADBCommand(ADBWrapper.__COMMAND_REBOOT)
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def waitForDevice(self) -> None:
        self.logger.info("WaitForDevice")
        cmdList = self.__createADBCommand(ADBWrapper.__COMMAND_WAIT_FOR_DEVICE)
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def waitForBootComplete(self) -> None:
        self.logger.info("WaitForBootComplete")
        cmdList = self.__createADBCommand(ADBWrapper.__COMMAND_WAIT_FOR_BOOT_COMPLETE)
        while True:
            result = subprocess.run(cmdList, stdout=subprocess.PIPE)
            self.logger.info(result)
            self.logger.info(result.stdout)
            if "1" in str(result.stdout):
                break
            else:
                time.sleep(3)

    def stopApp(self, app_id: str) -> None:
        self.logger.info("StopApp app_id={}".format(app_id))
        cmdList = self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_STOP_APP.format(app_id=app_id))
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def setScreenGrayScale(self, enabled: bool) -> None:
        if enabled:
            cmdList = self.__createADBCommand(
                ADBWrapper.__COMMAND_TEMPLATE_DISPLAY_DALTONIZER_ENABLED.format(enabled=1)
            )
            subprocess.run(cmdList, stdout=subprocess.DEVNULL)
            cmdList = self.__createADBCommand(
                ADBWrapper.__COMMAND_TEMPLATE_DISPLAY_DALTONIZER_GARY_SCALE
            )
            subprocess.run(cmdList, stdout=subprocess.DEVNULL)
        else:
            cmdList = self.__createADBCommand(
                ADBWrapper.__COMMAND_TEMPLATE_DISPLAY_DALTONIZER_ENABLED.format(enabled=0)
            )
            subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def pressBackButton(self) -> None:
        self.__keyEvent("KEYCODE_BACK")

    def pressEnterButton(self) -> None:
        self.__keyEvent("KEYCODE_ENTER")

    def pressSearchButton(self) -> None:
        self.__keyEvent("KEYCODE_SEARCH")

    def inputText(self, text: str) -> None:
        text = text.replace(" ", "%s")
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_INPUT_TEXT.format(text=text)
        )
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def __keyEvent(self, key_code: str) -> None:
        cmdList = self.__createADBCommand(
            ADBWrapper.__COMMAND_TEMPLATE_KEY_EVENT.format(key_code=key_code)
        )
        subprocess.run(cmdList, stdout=subprocess.DEVNULL)

    def logTouchPosition(self, timeout_second: int) -> None:
        self.logger.info("LogTouchPosition")
        command = self.__createADBCommand(ADBWrapper.__COMMAND_TEMPLATE_GET_EVENT)

        # サブプロセスを開始
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        Timer(timeout_second, process.terminate).start()
        latest_x = latest_y = None
        # 標準出力をリアルタイムで取得
        for line in iter(process.stdout.readline, ''):
            # 正規表現でパターンに基づいて分割
            pattern = r"\[|\]|\s+|:"
            parts = [p for p in re.split(pattern, line) if p]  # 空文字を除外
            if len(parts) == 5:
                if parts[3] == "BTN_TOUCH":
                    if parts[4] == "DOWN":
                        latest_x = latest_y = None

                elif parts[3] == "ABS_MT_POSITION_X":
                    if latest_x is not None:
                        continue
                    latest_x = int(parts[4], 16)
                elif parts[3] == "ABS_MT_POSITION_Y":
                    if latest_y is not None:
                        continue
                    latest_y = int(parts[4], 16)
                    if latest_x is not None and latest_y is not None:
                        self.logger.info("x={}, y={}".format(latest_x, latest_y))
        process.wait()

    def __createADBCommand(self, command_string: str) -> list[str]:
        commandPrefix = "adb "
        if self.deviceCode is not None:
            commandPrefix += "-s {} ".format(self.deviceCode)
        cmd = commandPrefix + command_string
        self.logger.info("cmd = {}".format(cmd))
        return cmd.split(" ")


if __name__ == "__main__":
    adb = ADBWrapper("37311FDJG009F5")
    adb.getPackageAndActivity()
    pass
