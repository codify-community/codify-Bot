from discord.ext import commands
from discord import app_commands, Member, Interaction, Client
from discord.ext.commands import Context

from use_cases.moderation.ban import BanUseCase, UnbanUseCase


class BanCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="banir", aliases=["ban"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: Context,
        membro: Member,
        motivo: str = "",
        deletar_mensagens: str = "0s",
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
    @app_commands.choices(
        deletar_mensagens=[
            app_commands.Choice(name="Não excluir nenhuma", value="0s"),
            app_commands.Choice(name="Última hora", value="1h"),
            app_commands.Choice(name="Últimas 6 horas", value="6h"),
            app_commands.Choice(name="Últimas 12 horas", value="12h"),
            app_commands.Choice(name="Últimas 24 horas", value="1d"),
            app_commands.Choice(name="Últimos 3 dias", value="3d"),
            app_commands.Choice(name="Últimos 7 dias", value="7d"),
        ]
    )
    async def ban_slash(
        self,
        interaction: Interaction,
        membro: Member,
        motivo: str = "",
        deletar_mensagens: app_commands.Choice[str] = "0s",
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
            deletar_mensagens.value,
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
        await unban_use_case.execute(interaction.guild, membro, motivo, self.client)


async def setup(client):
    await client.add_cog(BanCog(client))
