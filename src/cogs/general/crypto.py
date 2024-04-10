from discord.ext.commands import Context
from discord.ext import commands
from discord import Interaction, app_commands

from env import config
from use_cases.general.crypto import CryptoBuyUseCase, CryptoPricesUseCase


class CryptoCod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("criptopreços", aliases=["cprices", "cprecos"])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def precos(self, ctx):
        crypto_prices_use_case = CryptoPricesUseCase(
            send=ctx.send,
            author=ctx.author,
        )
        await crypto_prices_use_case.execute()

    group = app_commands.Group(
        name="cripto",
        description="...",
    )

    @commands.command("criptocomprar", aliases=["ccp", "cbuy"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def precos(self, ctx: Context, moeda: str, quantidade: str):
        crypto_buy_use_case = CryptoBuyUseCase(
            send=ctx.send,
            author=ctx.author,
        )
        await crypto_buy_use_case.execute(crypto=moeda, quantity=quantidade)

    @group.command(
        name="comprar",
        description="Compra uma criptomoeda.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.choices(
        moeda=[
            app_commands.Choice(name=config["crypto"]["names"][value], value=crypto)
            for crypto, value in config["crypto"]["abbreviation"].items()
        ]
    )
    async def comprar(
        self,
        interaction: Interaction,
        moeda: app_commands.Choice[str],
        quantidade: str,
    ):
        crypto_buy_use_case = CryptoBuyUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await crypto_buy_use_case.execute(
            crypto=moeda.value, quantity=quantidade, crypto_name=moeda.name
        )


async def setup(client):
    await client.add_cog(CryptoCod(client))
