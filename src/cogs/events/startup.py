from discord import Client, Game, Activity, ActivityType, Object
from asyncio import sleep
from discord.ext import commands


class StartupEventCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client
        self.activities = [
            Game(name="Codify Community"),
            Game(name="ilha das pythons 🐍"),
            Activity(
                type=ActivityType.listening,
                name="lofi enquanto corrijo bugs 🐜",
            ),
            Activity(type=ActivityType.watching, name="commits da Codify 🚀"),
        ]
        self.current_activity_index: int = 0

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("🚀 Discord bot running!")

        for guild in self.client.guilds:
            print(f"🕐 Syncing commands for {guild.name}")
            self.client.tree.copy_global_to(guild=Object(id=guild.id))
            await self.client.tree.sync(guild=Object(id=guild.id))

        print("🕐 All commands synced!")

        while True:
            activity = self.activities[self.current_activity_index]
            await self.client.change_presence(activity=activity)
            await sleep(30)
            self.current_activity_index = (self.current_activity_index + 1) % len(
                self.activities
            )


async def setup(client):
    await client.add_cog(StartupEventCog(client))
