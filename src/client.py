import os, discord
from discord.ext import commands

from env import env

# from utils.factories import (
#     PersistentTicketView,
#     PersistentTicketButtons,
#     PersistentTicketClosedButtons,
# )


class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=f"{'..' if env.environment == 'prod' else '!!'}",
            intents=discord.Intents.all(),
        )

    async def setup_hook(self):
        for i in os.listdir("./src/cogs"):
            for e in os.listdir(f"./src/cogs/{i}"):
                if str(e).endswith(".py"):
                    try:
                        await client.load_extension(f"cogs.{i}.{e[:-3]}")
                        print(f"✅ Cog loaded\t {i.capitalize()}/{e.capitalize()}")
                    except Exception:
                        print(f"❌ Cog failed\t {i.capitalize()}/{e.capitalize()}")

        # self.add_view(PersistentTicketView())
        # self.add_view(PersistentTicketButtons())
        # self.add_view(PersistentTicketClosedButtons())


client = MyClient()
client.run(env.token)
