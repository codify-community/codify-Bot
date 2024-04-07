import locale
from discord.ext import commands
from discord import Embed, Interaction, app_commands

from env import config
from repositories.cryptos_repository import CryptosRepository


class CryptoCod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.crypto_repository = CryptosRepository()

    group = app_commands.Group(
        name="cripto",
        description="...",
    )

    @group.command(
        name="preços",
        description="Mostra os preços das criptomoedas.",
    )
    async def historico_slash(self, interaction: Interaction):
        result = await self.crypto_repository.fetch_prices()
        prices = result["prices"]

        embed = Embed(title="Tabela de preços", color=0x9F6CFD)
        embed.set_author(
            name="Codify",
            icon_url=config["guild"]["icon"],
        )
        index = 0
        for crypto, data in prices.items():
            emoji = (
                config["guild"]["emojis"]["increase"]
                if data["status"] == "up"
                else config["guild"]["emojis"]["decrease"]
            )
            abbreviation = config["crypto"]["abbreviation"][crypto]
            name = config["crypto"]["names"][abbreviation]

            locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
            value = locale.currency(data["price"], grouping=True)

            embed.add_field(
                name=f"{emoji} {name} ({abbreviation})",
                value=value,
                inline=True,
            )
            index += 1

            if index % 2 == 0:
                embed.add_field(
                    name="\u200b", value="\u200b", inline=True
                )

        embed.set_footer(
            text=f"Última atualização em {result['updatedAt'].strftime('%d/%m/%Y às %H:%M:%S')}"
        )

        await interaction.response.send_message(embed=embed)


async def setup(client):
    await client.add_cog(CryptoCod(client))
