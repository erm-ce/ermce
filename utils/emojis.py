import os
import asyncio
import nest_asyncio

nest_asyncio.apply()  # dangerous!

default_emojis = {
    "check": 1439559595554111649,
    "xmark": 1439559593855418399,
    "success": 1439559576390209652,
    "error": 1439559590336401409,
    "WarningIcon": 1439559578462322749,
    "loa": 1439559585575866422,
    "log": 1439559571298324581,
    "shift": 1439559572992950313,
    "Clock": 1439559581750661152,
    "ShiftStarted": 1439559575002157096,
    "ShiftBreak": 1439559579859030148,
    "ShiftEnded": 1439559592169177252,
    "arrow": 1439559583394828290,
    "l_arrow": 1439559588163616902,
    "security": 1439559569893359636,
}


class EmojiController:
    def __init__(self, bot):
        self.environment = bot.environment
        self.bot = bot
        self.emojis = {}

    async def prefetch_emojis(self):

        application_emojis = await self.bot.fetch_application_emojis()
        for item in os.listdir("assets/emojis"):
            if item.endswith(".png"):
                if item.replace(".png", "") not in [i.name for i in application_emojis]:
                    emoji_name = item.replace(".png", "")
                    image_data = open(f"assets/emojis/{item}", "rb").read()
                    await self.bot.create_application_emoji(
                        name=emoji_name, image=image_data
                    )

        new_application_emojis = await self.bot.fetch_application_emojis()
        for emoji in new_application_emojis:
            self.emojis[emoji.name] = emoji.id

    def get_emoji(self, emoji_name):
        if not self.emojis:
            asyncio.run(self.prefetch_emojis())

        return "<:{}:{}>".format(emoji_name, self.emojis[emoji_name])
