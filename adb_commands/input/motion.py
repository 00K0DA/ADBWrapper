from dataclasses import dataclass
from ..base import ADBCommand

@dataclass
class Down(ADBCommand):
    x: int
    y: int

    @property
    def template(self) -> str:
        return "shell input motionevent DOWN {x} {y}"

    def format_command(self) -> str:
        return self.template.format(x=self.x, y=self.y)

@dataclass
class Up(ADBCommand):
    x: int
    y: int

    @property
    def template(self) -> str:
        return "shell input motionevent UP {x} {y}"

    def format_command(self) -> str:
        return self.template.format(x=self.x, y=self.y)

@dataclass
class Move(ADBCommand):
    x: int
    y: int

    @property
    def template(self) -> str:
        return "shell input motionevent MOVE {x} {y}"

    def format_command(self) -> str:
        return self.template.format(x=self.x, y=self.y) 