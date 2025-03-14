from dataclasses import dataclass
from ..base import ADBCommand

@dataclass
class Tap(ADBCommand):
    x: int
    y: int

    @property
    def template(self) -> str:
        return "shell input touchscreen tap {x} {y}"

    def format_command(self) -> str:
        return self.template.format(x=self.x, y=self.y)

@dataclass
class Swipe(ADBCommand):
    x1: int
    y1: int
    x2: int
    y2: int
    swipe_speed: int = 1000

    @property
    def template(self) -> str:
        return "shell input touchscreen swipe {x1} {y1} {x2} {y2} {swipe_speed}"

    def format_command(self) -> str:
        return self.template.format(
            x1=self.x1, y1=self.y1,
            x2=self.x2, y2=self.y2,
            swipe_speed=self.swipe_speed
        ) 