from discord.ext import commands
from discord import Message, Client

from env import config
from repositories.users_repository import UsersRepository

FIBO_BOT_ID = config["bots"]["fibo"]
GUILD_ID = config["guild"]["id"]


class MessageEventCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client
        self.user_repository = UsersRepository()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.content.startswith(self.client.user.mention):
            return await message.channel.send(
                f"{message.author.mention} | Meu prefixo é `..`!"
            )

        if message.author.id == FIBO_BOT_ID and message.guild.id == GUILD_ID:
            if message.content.startswith(
                "Thx for bumping our Server! We will remind you in 2 hours!"
            ):
                bumper = message.mentions[0]
                if not bumper:
                    return

                await self.user_repository.bump(bumper.id)
                return await message.add_reaction("🚀")

        # ToDO: Add level up system


async def setup(client):
    await client.add_cog(MessageEventCog(client))
