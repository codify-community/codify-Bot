from discord import Member, Guild
from use_cases.base import UseCase
from discord.utils import get

from env import config


class MuteUseCase(UseCase):
    async def execute(self, member: Member, bot: Member, guild: Guild):
        if member == bot:
            return await self.send_message(
                f"{self.author.mention} | Você não pode me mutar.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= self.author.top_role:
            return await self.send_message(
                f"{self.author.mention} | Você não pode mutar alguém com um cargo igual ou maior que o seu.",
                ephemeral=self.ephemeral,
            )

        mute_role = get(guild.roles, id=config["guild"]["roles"]["muted"])
        if not mute_role:
            return await self.send_message(
                f"{self.author.mention} | O cargo de mute não foi encontrado. Por favor, contate um administrador.",
                ephemeral=self.ephemeral,
            )

        if mute_role in member.roles:
            return await self.send_message(
                f"{self.author.mention} | O membro {member.name.capitalize()} já está mutado.",
                ephemeral=self.ephemeral,
            )

        await member.add_roles(mute_role)

        await self.send_message(
            f"{self.author.mention} | O membro {member.name.capitalize()} foi mutado com sucesso.",
            ephemeral=self.ephemeral,
        )


class UnmuteUseCase(UseCase):
    async def execute(self, member: Member, bot: Member, guild: Guild):
        if member == bot:
            return await self.send_message(
                f"{self.author.mention} | Você não pode me desmutar.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= self.author.top_role:
            return await self.send_message(
                f"{self.author.mention} | Você não pode desmutar alguém com um cargo igual ou maior que o seu.",
                ephemeral=self.ephemeral,
            )

        mute_role = get(guild.roles, id=config["guild"]["roles"]["muted"])
        if not mute_role:
            return await self.send_message(
                f"{self.author.mention} | O cargo de mute não foi encontrado. Por favor, contate um administrador.",
                ephemeral=self.ephemeral,
            )

        if mute_role not in member.roles:
            return await self.send_message(
                f"{self.author.mention} | O membro {member.name.capitalize()} não está mutado.",
                ephemeral=self.ephemeral,
            )

        await member.remove_roles(mute_role)

        await self.send_message(
            f"{self.author.mention} | O membro {member.name.capitalize()} foi desmutado com sucesso.",
            ephemeral=self.ephemeral,
        )
