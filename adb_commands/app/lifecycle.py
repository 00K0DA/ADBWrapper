from dataclasses import dataclass
from ..base import ADBCommand

@dataclass
class Launch(ADBCommand):
    app_id: str
    activity_name: str

    @property
    def template(self) -> str:
        return "shell am start -n {app_id}/{activity_name}"

    def format_command(self) -> str:
        return self.template.format(
            app_id=self.app_id,
            activity_name=self.activity_name
        )

@dataclass
class Stop(ADBCommand):
    app_id: str

    @property
    def template(self) -> str:
        return "shell am force-stop {app_id}"

    def format_command(self) -> str:
        return self.template.format(app_id=self.app_id) 