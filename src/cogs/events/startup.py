import discord
from asyncio import sleep
from discord.ext import commands


class StartupCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.activities = [
            discord.Game(name="Codify Community"),
            discord.Game(name="Ilha das Pithons 🐍"),
            discord.Activity(
                type=discord.ActivityType.listening,
                name="Lofi enquanto corrijo bugs 🐜"
            ),
            discord.Activity(
                type=discord.ActivityType.watching,
                name="Commits da Codify 🚀"
            ),
        ]
        self.current_activity_index = 0

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("🚀 Discord bot running!")

        for guild in self.client.guilds:
            print(f"🕐 Syncing commands for {guild.name}")
            self.client.tree.copy_global_to(guild=discord.Object(id=guild.id))
            await self.client.tree.sync(guild=discord.Object(id=guild.id))

        print("🕐 All commands synced!")

        while True:
            activity = self.activities[self.current_activity_index]
            await self.client.change_presence(activity=activity)
            await sleep(30)
            self.current_activity_index = (self.current_activity_index + 1) % len(
                self.activities
            )


async def setup(client):
    await client.add_cog(StartupCog(client))
