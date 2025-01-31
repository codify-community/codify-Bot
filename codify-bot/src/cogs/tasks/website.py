from typing import Self
from discord import Guild, User, Client
from discord.ext import commands, tasks

from env import config

from repositories.stats_repository import StatsRepository
from utils import get_updated_users, create_user_json


class WebsiteTasksCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client
        self.stats_repository = StatsRepository()

    @tasks.loop(minutes=10)
    async def get_info(self: Self) -> None:
        await self.client.wait_until_ready()
        guild: Guild = self.client.get_guild(config["guild"]["id"])

        if guild is None:
            print(
                "❌ Erro: Guild não encontrada! Verifique se o bot está no servidor correto."
            )
            return

        member_count = guild.member_count
        channel_count = len(guild.channels)

        db_staffs, db_boosters = await self.stats_repository.fetch_users_stats()
        discord_staffs, discord_boosters = [], []

        for member in guild.members:
            if member.bot:
                continue

            for role in reversed(member.roles):
                if role.id in config["guild"]["roles"]["staffs"]:
                    user: User = self.client.get_user(member.id)
                    staff = create_user_json(user, role)
                    discord_staffs.append(staff)
                    break
                elif role.id == config["guild"]["roles"]["booster"]:
                    user: User = self.client.get_user(member.id)
                    booster = create_user_json(user, role)
                    discord_boosters.append(booster)
                    break

        updated_staffs = get_updated_users(discord_staffs, db_staffs)
        updated_boosters = get_updated_users(discord_boosters, db_boosters)

        await self.stats_repository.update(
            channel_count, member_count, updated_staffs + updated_boosters
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print("🚀 Iniciando task de WebsiteTasksCog...")

        if not self.get_info.is_running():
            self.get_info.start()
            print("✅ Task `get_info` iniciada com sucesso!")
        else:
            print("⚠️ Task `get_info` já estava rodando!")


async def setup(client):
    await client.add_cog(WebsiteTasksCog(client))
