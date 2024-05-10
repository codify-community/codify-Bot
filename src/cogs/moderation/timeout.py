from discord.ext import commands
from discord import app_commands, Member, Client

from use_cases.moderation.timeout import TimeoutUseCase


class TimeoutCog(commands.Cog):
    def __init__(self, client: Client) -> None:
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
    @app_commands.choices(
        tempo=[
            app_commands.Choice(name="60 segundos", value="1m"),
            app_commands.Choice(name="5 minutos", value="5m"),
            app_commands.Choice(name="15 minutos", value="15m"),
            app_commands.Choice(name="30 minutos", value="30m"),
            app_commands.Choice(name="1 hora", value="1h"),
            app_commands.Choice(name="1 dia", value="1d"),
            app_commands.Choice(name="1 semana", value="7d"),
        ]
    )
    async def timeout_slash(
        self,
        interaction,
        membro: Member,
        tempo: app_commands.Choice[str],
        *,
        motivo: str = None
    ):
        timeout_use_case = TimeoutUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await timeout_use_case.execute(
            membro, interaction.guild.me, motivo, tempo.value
        )


async def setup(client):
    await client.add_cog(TimeoutCog(client))
