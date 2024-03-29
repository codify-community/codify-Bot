from discord.ext import commands
from discord import Member, app_commands

from use_cases.moderation.timeout import TimeoutUseCase


class TimeoutCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="castigar", aliases=["timeout"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def timeout(
        self, ctx, membro: Member, tempo: str = "1h", *, motivo: str = None
    ):
        timeout_use_case = TimeoutUseCase(send=ctx.send, author=ctx.author)
        await timeout_use_case.execute(membro, ctx.guild.me, motivo, tempo)

    @app_commands.command(
        name="castigar",
        description="Castiga um membro.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def timeout_slash(
        self, interaction, membro: Member, tempo: str = "1h", *, motivo: str = None
    ):
        timeout_use_case = TimeoutUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await timeout_use_case.execute(membro, interaction.guild.me, motivo, tempo)


async def setup(client):
    await client.add_cog(TimeoutCog(client))
