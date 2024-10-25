from discord import Member

from use_cases.base import UseCase
from utils import convert_to_seconds


class TimeoutUseCase(UseCase):

    async def execute(
        self, member: Member, bot: Member, reason: str, time: str
    ) -> None:
        if member == bot:
            return await self.send_message(
                f"{self.author.mention} | Você não pode me castigar.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= self.author.top_role:
            return await self.send_message(
                f"{self.author.mention} | Você não pode castigar alguém com um cargo igual ou maior que o seu.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= bot.top_role:
            return await self.send_message(
                f"{self.author.mention} | Eu não posso castigar alguém com um cargo igual ou maior que o meu.",
                ephemeral=self.ephemeral,
            )

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

        if seconds > 2_419_197:
            return await self.send_message(
                f"{self.author.mention} | O tempo inserido é muito longo. O máximo é 28 dias.",
                ephemeral=self.ephemeral,
            )

        await member.timeout(timedelta, reason=reason)
        await self.send_message(
            f"{self.author.mention} | {'O membro foi castigado com sucesso' if seconds > 0 else 'O membro teve o castigo removido com sucesso'}.",
            ephemeral=self.ephemeral,
        )
