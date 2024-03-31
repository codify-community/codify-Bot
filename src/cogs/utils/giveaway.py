from discord.ext import commands
from discord import app_commands, Interaction
from discord.ext.commands import Context

from use_cases.utils.giveaway import EndUseCase, GiveawayUseCase, RerollUseCase


class GiveawayCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="sorteio", aliases=["giveaway"])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def giveaway(
        self,
        ctx: Context,
        nome: str,
        tempo: str,
        descrição: str = "",
        requisitos: str = None,
        vencedores: int = 1,
        image: str = None,
    ):
        giveaway_use_case = GiveawayUseCase(send=ctx.send, author=ctx.author)
        await giveaway_use_case.execute(
            ctx.channel, nome, tempo, descrição, requisitos, vencedores, image
        )

    group = app_commands.Group(
        name="sorteio",
        description="...",
    )

    @group.command(
        name="iniciar",
        description="Inicia um sorteio.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.guild.id)
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def giveaway_slash(
        self,
        interaction: Interaction,
        nome: str,
        tempo: str,
        descrição: str = "",
        requisitos: str = None,
        vencedores: int = 1,
        image: str = None,
    ):
        giveaway_use_case = GiveawayUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await giveaway_use_case.execute(
            interaction.channel,
            nome,
            tempo,
            descrição,
            requisitos,
            vencedores,
            image,
        )

    @commands.command(name="reroll", aliases=["sortearnovamente"])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def reroll(self, ctx: Context, sorteio_id: str, vencedores: int = None):
        reroll_use_case = RerollUseCase(send=ctx.send, author=ctx.author)
        await reroll_use_case.execute(ctx.channel, sorteio_id, vencedores, self.client)

    @group.command(
        name="resortear",
        description="Sorteia novamente um sorteio.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.guild.id)
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def reroll_slash(
        self, interaction: Interaction, sorteio_id: str, vencedores: int = None
    ):
        reroll_use_case = RerollUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await reroll_use_case.execute(
            interaction.channel, sorteio_id, vencedores, self.client
        )

    @commands.command(name="end", aliases=["terminar"])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def end(self, ctx: Context, sorteio_id: str):
        end_use_case = EndUseCase(send=ctx.send, author=ctx.author)
        await end_use_case.execute(ctx.channel, sorteio_id)

    @group.command(
        name="terminar",
        description="Termina um sorteio.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.guild.id)
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def end_slash(self, interaction: Interaction, sorteio_id: str):
        end_use_case = EndUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await end_use_case.execute(interaction.channel, sorteio_id)


async def setup(client):
    await client.add_cog(GiveawayCog(client))
