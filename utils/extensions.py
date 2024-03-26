from utils.bot import Xeno
from typing import List

class DefaultExtensions:
    def __init__(self):
        self.extensions: List[str] = [
            "cogs.info"
        ]
        
    async def load_all_extensions(self, bot: Xeno):
        for extension in self.extensions:
            try:
                await bot.load_extension(extension)
                print(f"Loaded extension: {extension}")
            except Exception as e:
                print(f"Failed to load extension {extension}.")
                print(e)