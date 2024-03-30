from discord.ext import commands
from discord import app_commands, Interaction
from discord.ext.commands import Context

from use_cases.moderation.lock import LockUseCase


class LockCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="trancar", aliases=["lock"])
    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.has_permissions(manage_messages=True)
    async def lock(self, ctx: Context) -> None:
        lock_use_case = LockUseCase(send=ctx.send, author=ctx.author)
        await lock_use_case.execute(ctx.channel, ctx.guild.default_role)

    @app_commands.command(
        name="trancar",
        description="Tranca e destranca um canal.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.channel.id)
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def lock_slash(self, interaction: Interaction) -> None:
        lock_use_case = LockUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await lock_use_case.execute(interaction.channel, interaction.guild.default_role)


async def setup(client):
    await client.add_cog(LockCog(client))
