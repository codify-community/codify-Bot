from discord import Embed

from env import config
from repositories.users_repository import users_repository
from use_cases.base import UseCase


class TopBumpersUseCase(UseCase):

    async def execute(self):
        top_bumpers = await users_repository.get_bumpers()

        embed = Embed(title="Top bumpers", color=0x9F6CFD, description="")
        embed.set_thumbnail(url=config["guild"]["icon"])
        for place, user in enumerate(top_bumpers, start=1):
            embed.description += (
                f"**{place}º** <@{user['_id']}> com {user['bumpCount']} bumps\n"
            )
        await self.send_message(embed=embed)
