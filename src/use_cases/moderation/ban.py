from discord import Member, Guild, Client, errors

from use_cases.base import UseCase
from utils.utils import convert_to_seconds


class BanUseCase(UseCase):

    async def execute(
        self,
        member: Member,
        bot: Member,
        reason: str,
        delete_after: str,
    ) -> None:
        try:
            _, seconds, _ = convert_to_seconds(delete_after)
        except ValueError as e:
            return await self.send_message(
                f"{self.author.mention} | O tempo inserido é inválido. {e}",
                ephemeral=self.ephemeral,
            )

        if seconds > 604_800 or seconds < 0:
            return await self.send_message(
                f"{self.author.mention} | Só é possível deletar mensagens de até 7 dias atrás.",
                ephemeral=self.ephemeral,
            )

        if member == bot:
            return await self.send_message(
                f"{self.author.mention} | Você não pode me banir.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= self.author.top_role:
            return await self.send_message(
                f"{self.author.mention} | Você não pode banir alguém com um cargo igual ou maior que o seu.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= bot.top_role:
            return await self.send_message(
                f"{self.author.mention} | Eu não posso banir alguém com um cargo igual ou maior que o meu.",
                ephemeral=self.ephemeral,
            )

        try:
            await member.ban(reason=reason, delete_message_seconds=seconds)
        except:
            return await self.send_message(
                f"{self.author.mention} | Ocorreu um erro ao banir o membro.",
                ephemeral=self.ephemeral,
            )

        await self.send_message(
            f"{self.author.mention} | O membro {member.name.capitalize()} foi banido com sucesso.",
            ephemeral=self.ephemeral,
        )


class UnbanUseCase(UseCase):

    async def execute(
        self,
        guild: Guild,
        member: str,
        reason: str,
        client: Client,
    ) -> None:
        try:
            member = await client.fetch_user(member)
            await guild.unban(member, reason=reason)
        except errors.NotFound:
            return await self.send_message(
                f"{self.author.mention} | O membro não está banido.",
                ephemeral=self.ephemeral,
            )
        except:
            return await self.send_message(
                f"{self.author.mention} | Ocorreu um erro ao desbanir o membro.",
                ephemeral=self.ephemeral,
            )

        await self.send_message(
            f"{self.author.mention} | O membro {member.name.capitalize()} foi desbanido com sucesso.",
            ephemeral=self.ephemeral,
        )
