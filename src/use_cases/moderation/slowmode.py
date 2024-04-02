from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from discord.abc import MessageableChannel

from use_cases.base import UseCase
from utils import convert_to_seconds


class SlowmodeUseCase(UseCase):

    async def execute(self, channel: "MessageableChannel", time: str):
        try:
            _, seconds, timedelta = convert_to_seconds(time)
        except ValueError as e:
            return await self.send_message(
                f"{self.author.mention} | O tempo inserido é inválido. {e}",
                ephemeral=self.ephemeral,
            )

        if seconds < 0:
            return await self.send_message(
                f"{self.author.mention} | O tempo inserido é muito pequeno. O mínimo é 0 segundos.",
                ephemeral=self.ephemeral,
            )

        if seconds > 21_600:
            return await self.send_message(
                f"{self.author.mention} | O tempo inserido é muito longo, o máximo é 6 horas.",
                ephemeral=self.ephemeral,
            )

        await channel.edit(slowmode_delay=seconds)
        await self.send_message(
            f"{self.author.mention} | {f'Slow mode definido para {timedelta}' if seconds > 0 else 'Slow mode desativado'}.",
            ephemeral=self.ephemeral,
        )
