from dataclasses import dataclass
from ..base import ADBCommand

@dataclass
class ConnectWireless(ADBCommand):
    ip_address: str
    port: str

    @property
    def template(self) -> str:
        return "connect {ip_address}:{port}"

    def format_command(self) -> str:
        return self.template.format(
            ip_address=self.ip_address,
            port=self.port
        ) 