from discord.ext import commands
from discord import app_commands, Member, Interaction, Client
from discord.ext.commands import Context

from use_cases.moderation.kick import KickUseCase


class KickCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="expulsar", aliases=["kick"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: Context, membro: Member, motivo: str = None) -> None:
        kick_use_case = KickUseCase(send=ctx.send, author=ctx.author)
        await kick_use_case.execute(membro, ctx.guild.me, motivo)

    @app_commands.command(
        name="expulsar",
        description="Expulsa um membro.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.default_permissions(kick_members=True)
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_slash(
        self, interaction: Interaction, membro: Member, motivo: str = None
    ) -> None:
        kick_use_case = KickUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await kick_use_case.execute(membro, interaction.guild.me, motivo)


async def setup(client):
    await client.add_cog(KickCog(client))
