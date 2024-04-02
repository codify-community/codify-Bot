from discord import Guild, User
from discord.ext import commands, tasks

from env import config

from repositories.stats_repository import stats_repository
from utils import get_updated_users, create_user_json


class WebsiteTasksCog(commands.Cog):
    def __init__(self, client):
        self.client = client

        @tasks.loop(minutes=10)
        async def get_info(self):
            await self.client.wait_until_ready()
            guild: Guild = self.client.get_guild(config["guild"]["id"])

            member_count = int(guild.member_count)
            channel_count = len(guild.channels)

            db_staffs, db_boosters = await stats_repository.fetch_users_stats()
            discord_staffs, discord_boosters = [], []

            for member in guild.members:
                if member.bot:
                    continue

                for role in reversed(member.roles):
                    if role.id in config["guild"]["roles"]["staffs"]:
                        user: User = await self.client.fetch_user(member.id)
                        staff = create_user_json(user, role)

                        discord_staffs.append(staff)
                        break

                    elif role.id == config["guild"]["roles"]["booster"]:
                        user: User = await self.client.fetch_user(member.id)
                        booster = create_user_json(user, role)

                        discord_boosters.append(booster)
                        break

            updated_staffs = get_updated_users(discord_staffs, db_staffs)
            updated_boosters = get_updated_users(discord_boosters, db_boosters)

            await stats_repository.update(
                channel_count, member_count, updated_staffs + updated_boosters
            )

        get_info.start(self)


async def setup(client):
    await client.add_cog(WebsiteTasksCog(client))
