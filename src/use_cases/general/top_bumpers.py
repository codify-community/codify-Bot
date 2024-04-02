from discord import Embed

from env import config
from repositories.users_repository import UsersRepository
from use_cases.base import UseCase


class TopBumpersUseCase(UseCase):
    def __init__(self, send, author, ephemeral=False):
        super().__init__(send, author, ephemeral)
        self.user_repository = UsersRepository()

    async def execute(self):
        top_bumpers = await self.user_repository.get_bumpers()

        embed = Embed(title="Top bumpers", color=0x9F6CFD, description="")
        embed.set_thumbnail(url=config["guild"]["icon"])
        for place, user in enumerate(top_bumpers, start=1):
            embed.description += f"**{place}º** <@{user['_id']}> com {user['bumpCount']} {'bumps' if user['bumpCount'] > 1 else 'bump'}!\n"
        await self.send_message(embed=embed)
