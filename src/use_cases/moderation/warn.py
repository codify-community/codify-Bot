from discord import ButtonStyle, Interaction, Member

from use_cases.base import UseCase
from utils.database import userDatabase
from utils.embed import create_warns_embed
from utils.factories import CustomButton, CustomView


class WarnUseCase(UseCase):

    async def execute(self, member: Member, bot: Member, reason: str):
        if member.bot:
            return await self.send_message(
                f"{self.author.mention} | Você não pode usar este comando em bots.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= self.author.top_role:
            return await self.send_message(
                f"{self.author.mention} | Você não pode adicionar warns em membros com cargos iguais ou superiores ao seu.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= bot.top_role:
            return await self.send_message(
                f"{self.author.mention} | Eu não posso adicionar warns em membros com cargos iguais ou superiores ao meu.",
                ephemeral=self.ephemeral,
            )

        await userDatabase.get_user(member.id)
        await userDatabase.add_warn(member.id, reason)

        await self.send_message(
            f"{self.author.mention} | O warn foi adicionado com sucesso.",
            ephemeral=self.ephemeral,
        )


class UnwarnUseCase(UseCase):

    async def execute(self, member: Member, bot: Member, warn_id: str):
        if member.bot:
            return await self.send_message(
                f"{self.author.mention} | Você não pode usar este comando em bots.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= self.author.top_role:
            return await self.send_message(
                f"{self.author.mention} | Você não pode remover warns de membros com cargos iguais ou superiores ao seu.",
                ephemeral=self.ephemeral,
            )

        if member.top_role >= bot.top_role:
            return await self.send_message(
                f"{self.author.mention} | Eu não posso remover warns de membros com cargos iguais ou superiores ao meu.",
                ephemeral=self.ephemeral,
            )

        await userDatabase.get_user(member.id)

        try:
            await userDatabase.remove_warn(member.id, warn_id)
        except ValueError:
            return await self.send_message(
                f"{self.author.mention} | O warn não foi encontrado.",
                ephemeral=self.ephemeral,
            )

        await self.send_message(
            f"{self.author.mention} | O warn foi removido com sucesso.",
            ephemeral=self.ephemeral,
        )


class WarnsUseCase(UseCase):

    async def execute(self, member: Member, bot: Member):
        if member.bot:
            return await self.send_message(
                f"{self.author.mention} | Você não pode usar este comando em bots.",
                ephemeral=self.ephemeral,
            )

        warns = await userDatabase.get_warns(member.id)
        if warns["count"] == 0:
            return await self.send_message(
                f"{self.author.mention} | O membro não possui warns.",
                ephemeral=self.ephemeral,
            )

        current_page = 1
        total_pages = (warns["count"] + 4) // 5
        embed = create_warns_embed(member, warns, current_page)

        buttons = [
            CustomButton(
                style=ButtonStyle.gray,
                label="⬅️ Página Anterior",
                custom_id="previus_page",
                disabled=True,
            ),
            CustomButton(
                style=ButtonStyle.gray,
                label="Próxima Página ➡️",
                custom_id="next_page",
                disabled=True if total_pages == 1 else False,
            ),
        ]

        context = {
            "total_pages": total_pages,
            "current_page": current_page,
            "member": member,
        }

        async def button_callback(button_interaction: Interaction):
            if button_interaction.user.id != self.author.id:
                return await button_interaction.response.send_message(
                    f"{self.author.mention} | Você não pode usar este botão!",
                    ephemeral=self.ephemeral,
                )

            context["current_page"] += (
                1 if button_interaction.data["custom_id"] == "next_page" else -1
            )

            warns = await userDatabase.get_warns(
                context["member"].id, page=context["current_page"]
            )

            buttons[0].disabled = True if context["current_page"] == 1 else False
            buttons[1].disabled = (
                True if context["current_page"] == total_pages else False
            )

            return await button_interaction.response.edit_message(
                embed=create_warns_embed(member, warns, context["current_page"]),
                view=view,
            )

        for button in buttons:
            button.callback = button_callback

        view = CustomView(buttons=buttons, timeout=30)
        await self.send_message(embed=embed, view=view, ephemeral=True)
