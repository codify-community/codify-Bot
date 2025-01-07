import locale
from discord import Embed, ButtonStyle, Interaction
from repositories.cryptos_repository import CryptosRepository

from env import config
from repositories.users_repository import UsersRepository
from use_cases.base import UseCase
from utils.factories import CustomButton, CustomView

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


class CryptoPricesUseCase(UseCase):
    def __init__(self, send, author, ephemeral=False) -> None:
        super().__init__(send, author, ephemeral)
        self.crypto_repository = CryptosRepository()

    async def execute(self):
        result = await self.crypto_repository.fetch_prices()
        prices = result["prices"]

        embed = Embed(title="Tabela de preços", color=0x9F6CFD)
        index = 0
        for crypto, data in prices.items():
            emoji = (
                config["guild"]["emojis"]["increase"]
                if data["status"] == "up"
                else config["guild"]["emojis"]["decrease"]
            )
            abbreviation = config["crypto"]["abbreviation"][crypto]
            name = config["crypto"]["names"][abbreviation]

            value = locale.currency(data["price"], grouping=True)

            embed.add_field(
                name=f"{emoji} {name} ({abbreviation})",
                value=value,
                inline=True,
            )
            index += 1

            if index % 2 == 0:
                embed.add_field(name="\u200b", value="\u200b", inline=True)

        embed.set_footer(
            text=f"Última atualização em {result['updatedAt'].strftime('%d/%m/%Y às %H:%M:%S')}"
        )

        await self.send_message(embed=embed)


class CryptoBuyUseCase(UseCase):
    def __init__(self, send, author, ephemeral=False) -> None:
        super().__init__(send, author, ephemeral)
        self.crypto_repository = CryptosRepository()
        self.user_repository = UsersRepository()

    async def execute(self, crypto: str, quantity: str, crypto_name: str = None):
        if crypto not in config["crypto"]["abbreviation"]:
            return await self.send_message(
                f"{self.author.mention} | Moeda inválida. Informe a moeda pela sigla. Ex BTCBRL.",
                ephemeral=self.ephemeral,
            )

        try:
            quantity = float(quantity)
        except ValueError:
            return await self.send_message(
                f"{self.author.mention} | A quantidade deve ser um número.",
                ephemeral=self.ephemeral,
            )

        if quantity <= 0:
            return await self.send_message(
                f"{self.author.mention} | A quantidade deve ser maior que 0.",
                ephemeral=self.ephemeral,
            )

        if len(str(quantity).split(".")[1]) > 2:
            return await self.send_message(
                f"{self.author.mention} | A quantidade deve ter até 2 casas decimais.",
                ephemeral=self.ephemeral,
            )

        result = await self.crypto_repository.fetch_prices()
        prices = result["prices"]
        price = prices[crypto]["price"] * quantity

        if not crypto_name:
            crypto_name = config["crypto"]["names"][
                config["crypto"]["abbreviation"][crypto]
            ]

        buttons = [
            CustomButton(
                style=ButtonStyle.success,
                label="Confirmar",
                custom_id="cript_buy_confirm",
            ),
            CustomButton(
                style=ButtonStyle.danger,
                label="Cancelar",
                custom_id="cript_buy_cancel",
            ),
        ]

        async def buy_confirmation(button_interaction: Interaction):
            if button_interaction.user.id != self.author.id:
                return await button_interaction.response.send_message(
                    f"{self.author.mention} | Você não pode usar este botão!",
                    ephemeral=True,
                )

            user = await self.user_repository.get_user(self.author.id)
            if user["patrimony"] < price:
                return await button_interaction.response.edit_message(
                    content=f"{self.author.mention} | Você não tem saldo suficiente para comprar {quantity} {crypto_name}.",
                    view=CustomView(buttons=buttons, buttons_disabled=True),
                )

            user["patrimony"] -= price
            user["wallet"][crypto] = user["wallet"].get(crypto, 0) + quantity

            await self.user_repository.update_user(button_interaction.user.id, user)

            return await button_interaction.response.edit_message(
                content=f"{self.author.mention} | Compra realizada com sucesso!",
                view=CustomView(buttons=buttons, buttons_disabled=True),
            )

        async def buy_decline(button_interaction: Interaction):
            if button_interaction.user.id != self.author.id:
                return await button_interaction.response.send_message(
                    f"{self.author.mention} | Você não pode usar este botão!",
                    ephemeral=True,
                )

            return await button_interaction.response.edit_message(
                content=f"{self.author.mention} | Compra cancelada.",
                view=CustomView(buttons=buttons, buttons_disabled=True),
            )

        buttons[0].callback = buy_confirmation
        buttons[1].callback = buy_decline

        value = locale.currency(price, grouping=True)

        return await self.send_message(
            f"{self.author.mention} | Você está prestes a comprar {quantity} {crypto_name} por {value}.",
            view=CustomView(buttons=buttons),
            ephemeral=self.ephemeral,
        )
