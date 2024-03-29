from discord.ext import commands
from discord import app_commands, Member, Interaction
from discord.ext.commands import Context

from use_cases.moderation.ban import BanUseCase, UnbanUseCase


class BanCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="banir", aliases=["ban"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: Context,
        membro: Member,
        motivo: str = "",
        deletar_mensagens: int = 0,
    ) -> None:
        ban_use_case = BanUseCase(send=ctx.send, author=ctx.author)
        await ban_use_case.execute(
            membro,
            ctx.guild.me,
            motivo,
            deletar_mensagens,
        )

    @app_commands.command(
        name="banir",
        description="Bane um membro.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_slash(
        self,
        interaction: Interaction,
        membro: Member,
        motivo: str = "",
        deletar_mensagens: int = 0,
    ) -> None:
        ban_use_case = BanUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await ban_use_case.execute(
            membro,
            interaction.guild.me,
            motivo,
            deletar_mensagens,
        )

    @commands.command(name="desbanir", aliases=["unban"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx: Context, membro: str, motivo: str = "") -> None:
        unban_use_case = UnbanUseCase(send=ctx.send, author=ctx.author)
        await unban_use_case.execute(ctx.guild, membro, motivo, self.client)

    @app_commands.command(
        name="desbanir",
        description="Retira o banimento de um membro.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.default_permissions(ban_members=True)
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban_slash(
        self, interaction: Interaction, membro: str, motivo: str = ""
    ) -> None:
        unban_use_case = UnbanUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await unban_use_case.execute(
            interaction.guild, membro, motivo, self.client
        )


async def setup(client):
    await client.add_cog(BanCog(client))
