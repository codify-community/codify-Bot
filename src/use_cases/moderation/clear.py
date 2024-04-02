from typing import TYPE_CHECKING
from discord import InteractionResponse

if TYPE_CHECKING:
    from discord.abc import MessageableChannel

from use_cases.base import UseCase


class ClearUseCase(UseCase):

    async def execute(
        self,
        channel: "MessageableChannel",
        quantity: int,
        response: InteractionResponse = None,
    ) -> None:
        if quantity > 100:
            return await self.send_message(
                f"{self.author.mention} | Você não pode limpar mais de 100 mensagens.",
                ephemeral=self.ephemeral,
            )

        if quantity < 1:
            return await self.send_message(
                f"{self.author.mention} | Você não pode limpar menos de 1 mensagem.",
                ephemeral=self.ephemeral,
            )

        if self.ephemeral:
            await response.defer()

        await channel.purge(limit=quantity + 1)
