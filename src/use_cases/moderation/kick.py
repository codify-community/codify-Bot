from discord import Member

from use_cases.base import UseCase


class KickUseCase(UseCase):
    async def execute(
        self,
        member: Member,
        bot: Member,
        reason: str,
    ):
        if member == bot:
            return await self.send_message(
                f"{self.author.mention} | Você não pode me expulsar.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= self.author.top_role:
            return await self.send_message(
                f"{self.author.mention} | Você não pode expulsar alguém com um cargo igual ou maior que o seu.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= bot.top_role:
            return await self.send_message(
                f"{self.author.mention} | Eu não posso expulsar alguém com um cargo igual ou maior que o meu.",
                ephemeral=self.ephemeral,
            )

        await member.kick(reason=reason)

        await self.send_message(
            f"{self.author.mention} | O membro {member.name.capitalize()} foi expulso com sucesso.",
            ephemeral=self.ephemeral,
        )
