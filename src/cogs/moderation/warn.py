from discord.ext import commands
from discord import app_commands, Member, Interaction
from discord.ext.commands import Context


from use_cases.moderation.warn import UnwarnUseCase, WarnUseCase, WarnsUseCase


class WarnCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="avisar", aliases=["warn"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx: Context, membro: Member, motivo: str = None) -> None:
        warn_use_case = WarnUseCase(send=ctx.send, author=ctx.author)
        await warn_use_case.execute(membro, ctx.guild.me, motivo)

    group = app_commands.Group(
        name="avisos",
        description="...",
    )

    @group.command(
        name="adicionar",
        description="Adiciona um warn no membro.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn_slash(
        self, interaction: Interaction, membro: Member, motivo: str = None
    ) -> None:
        warn_use_case = WarnUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await warn_use_case.execute(membro, interaction.guild.me, motivo)

    @commands.command(name="removeraviso", aliases=["unwarn"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def unwarn(self, ctx: Context, membro: Member, aviso_id: str) -> None:
        unwarn_use_case = UnwarnUseCase(send=ctx.send, author=ctx.author)
        await unwarn_use_case.execute(membro, ctx.guild.me, aviso_id)

    @group.command(
        name="remover",
        description="Remove um warn do membro.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def unwarn_slash(
        self, interaction: Interaction, membro: Member, aviso_id: str
    ) -> None:
        unwarn_use_case = UnwarnUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await unwarn_use_case.execute(membro, interaction.guild.me, aviso_id)

    @commands.command(name="avisos", aliases=["warns"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def warns(self, ctx: Context, membro: Member) -> None:
        warns_use_case = WarnsUseCase(send=ctx.send, author=ctx.author)
        await warns_use_case.execute(membro, ctx.guild.me)

    @group.command(
        name="mostrar",
        description="Mostra os warns do membro.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warns_slash(self, interaction: Interaction, membro: Member) -> None:
        warns_use_case = WarnsUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await warns_use_case.execute(membro, interaction.guild.me)


async def setup(client):
    await client.add_cog(WarnCog(client))
