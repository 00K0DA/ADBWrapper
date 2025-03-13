from DiscordNotificator import DiscordNotificator, DiscordMessage


class PokePokeDiscordNotificator(DiscordNotificator):
    web_hook_url = "https://discord.com/api/webhooks/1349750576853946379/SBGwIGFAl8cH0zMfotp0SHoQyufKZWCTtoSJHRipcktzwNe16Pk9ASkiSjz3tONusSc7"

    def __init__(self):
        super().__init__(self.web_hook_url)

    def send_message(self, discord_message: DiscordMessage) -> None:
        super().send_message(discord_message)
