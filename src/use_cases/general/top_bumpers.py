from datetime import datetime
from discord import Client, Embed, Guild

from env import config
from repositories.users_repository import UsersRepository
from use_cases.base import UseCase


class TopBumpersUseCase(UseCase):
    def __init__(self, send, author, ephemeral=False) -> None:
        super().__init__(send, author, ephemeral)
        self.user_repository = UsersRepository()

    async def execute(self, guild: Guild, client: Client):
        top_bumpers = await self.user_repository.get_bumpers()

        if not top_bumpers:
            embed.description = "Ninguém bumpou ainda!"
            return await self.send_message(embed=embed)

        embed = Embed(title="🏆 Top Bumpers", color=0x9F6CFD, description="")
        embed.set_thumbnail(url=config["guild"]["icon"])

        for place, user in enumerate(top_bumpers, start=1):
            isUserInGuild = guild.get_member(user["_id"])
            if isUserInGuild:
                mention = isUserInGuild.mention
            else:
                current_user = await client.fetch_user(user["_id"])
                mention = current_user.name.capitalize()

            embed.description += f"**{place}º** {mention} com {user['bumpCount']} {'bumps' if user['bumpCount'] > 1 else 'bump'}!\n"

        embed.set_footer(text=datetime.now().strftime("%d/%m/%Y as %H:%M"))
        await self.send_message(embed=embed)
