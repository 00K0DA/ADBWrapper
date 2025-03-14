from dataclasses import dataclass
from ..base import ADBCommand

@dataclass
class Take(ADBCommand):
    @property
    def template(self) -> str:
        return "shell screencap -p /sdcard/screen_shot_temp.png"

    def format_command(self) -> str:
        return self.template

@dataclass
class Sync(ADBCommand):
    @property
    def template(self) -> str:
        return "shell sync"

    def format_command(self) -> str:
        return self.template

@dataclass
class Pull(ADBCommand):
    path: str

    @property
    def template(self) -> str:
        return "pull /sdcard/screen_shot_temp.png {path}"

    def format_command(self) -> str:
        return self.template.format(path=self.path)

@dataclass
class Remove(ADBCommand):
    @property
    def template(self) -> str:
        return "shell rm /sdcard/screen_shot_temp.png"

    def format_command(self) -> str:
        return self.template 