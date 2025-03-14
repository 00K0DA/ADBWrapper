from dataclasses import dataclass
from ..base import ADBCommand

@dataclass
class Reboot(ADBCommand):
    @property
    def template(self) -> str:
        return "reboot"

    def format_command(self) -> str:
        return self.template

@dataclass
class WaitForDevice(ADBCommand):
    @property
    def template(self) -> str:
        return "wait-for-device"

    def format_command(self) -> str:
        return self.template

@dataclass
class WaitForBootComplete(ADBCommand):
    @property
    def template(self) -> str:
        return "shell getprop sys.boot_completed"

    def format_command(self) -> str:
        return self.template 