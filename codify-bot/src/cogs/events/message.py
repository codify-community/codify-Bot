from discord.ext import commands
from discord import Message, Client

from env import config
from repositories.users_repository import UsersRepository


FIBO_BOT_ID = config["bots"]["fibo"]
GUILD_ID = config["guild"]["id"]

PRESENTATION_CHANNEL_ID = config["guild"]["channels"]["presentation"]


class MessageEventCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client
        self.user_repository = UsersRepository()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.channel.id == PRESENTATION_CHANNEL_ID:
            pass

            # user_message_history = [
            #     message
            #     async for message in message.channel.history(limit=10)
            #     if message.author.id == message.author.id
            # ]

            # if len(user_message_history) > 1:
            #     return

            # await message.add_reaction("👋")

        elif message.author.id == FIBO_BOT_ID and message.guild.id == GUILD_ID:
            if message.content.startswith(
                "Thx for bumping our Server! We will remind you in 2 hours!"
            ):
                bumper = message.mentions[0]
                if not bumper:
                    return

                await self.user_repository.bump(bumper.id)
                return await message.add_reaction("🚀")

        elif message.content.startswith(self.client.user.mention):
            return await message.channel.send(
                f"{message.author.mention} | Meu prefixo é `..`!"
            )

        # ToDO: Add level up system


async def setup(client):
    await client.add_cog(MessageEventCog(client))
