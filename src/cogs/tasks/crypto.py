import requests
from discord.ext import commands
from discord.ext import tasks

from repositories.crypto_repository import cryptoRepository

cryptos = {
    "BTC": "BTCBRL",
    "ETH": "ETHBRL",
    "BNB": "BNBBRL",
    "LTC": "LTCBRL",
    "AXS": "AXSBRL",
    "SOL": "SOLBRL",
    "DOT": "DOTBRL",
    "LINK": "LINKBRL",
    "CAKE": "CAKEBRL",
}


class CriptoTasksCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(minutes=5)
    async def get_cripto_prices():
        symbols = [f"%22{cripto}%22" for cripto in cryptos.values()]
        url = (
            f'https://www.binance.me/api/v3/ticker/price?symbols=[{",".join(symbols)}]'
        )
        response = requests.get(url)
        data = response.json()

        await cryptoRepository.update_prices(data)

    get_cripto_prices.start()


async def setup(client):
    await client.add_cog(CriptoTasksCog(client))
