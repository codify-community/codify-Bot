from discord import Member, Client
from discord.ext import commands


class WelcomeEventCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        pass


async def setup(client):
    await client.add_cog(WelcomeEventCog(client))
