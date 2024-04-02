import discord, datetime
from asyncio import sleep
from discord.ui import View, Select, Button, select
from discord import Embed
from discord.utils import get

from env import config
from utils import is_user_staff


class CustomView(View):
    def __init__(self, timeout: int = None, selects: list = None, buttons: list = None):
        super().__init__(timeout=timeout)

        if selects:
            for select in selects:
                self.add_item(select)

        if buttons:
            for button in buttons:
                self.add_item(button)


class CustomSelect(Select):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PersistentViewBase(View):
    def __init__(self):
        super().__init__(timeout=None)

    def disable_buttons(self):
        for child in self.children:
            child.disabled = True
        return self


class PersistentTicketView(PersistentViewBase):
    @select(
        custom_id="ticket_select",
        placeholder="Selecione uma opção...",
        options=[
            discord.SelectOption(
                label="Dúvida",
                emoji="📝",
                description="Tirar dúvidas",
            ),
            discord.SelectOption(
                label="Financeiro",
                emoji="💸",
                description="Falar com a equipe de finanças",
            ),
            discord.SelectOption(
                label="Suporte",
                emoji="⚒️",
                description="Entrar em contato com a equipe de suporte",
            ),
            discord.SelectOption(
                label="Denúncia",
                emoji="🚨",
                description="Reportar um jogador ou membro da equipe",
            ),
        ],
    )
    async def select_callback(self, select, item):
        await select.message.edit(view=self)

        now = datetime.datetime.now()

        overwrites = {
            select.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            select.user: discord.PermissionOverwrite(
                view_channel=True, send_messages=True
            ),
        }

        category = get(
            select.guild.categories, id=config["guild"]["channels"]["ticket"]
        )
        channel = await category.create_text_channel(
            f"ticket-{item.values[0].lower()}-{datetime.datetime.now().strftime('%d%m%y')}-{select.user.id}",
            topic=f"Data de abertura {now.strftime('%d/%m/%Y as %H:%M')} | Motivo: {item.values[0]}",
            overwrites=overwrites,
        )

        embed = Embed(
            title=f"Atendimento | {item.values[0]} - NRRP",
            description=f"Olá, {select.user.name.capitalize()}!\nEnvie sua dúvida ou denuncia que nossa equipe já irá te atender.",
            color=0x9F6CFD,
        )
        embed.set_thumbnail(url=config["guild"]["icon"])
        embed.set_footer(text="Se não quiser mais ser atendido tranque o ticket!")
        buttons = PersistentTicketButtons()

        await channel.send(select.user.mention, embed=embed, view=buttons)

        await select.response.send_message(
            embed=Embed(
                title=f"Ticket de {item.values[0]} aberto!",
                description=f"{select.user.mention}, seu ticket foi aberto com sucesso!",
                color=0x9F6CFD,
            ),
            ephemeral=True,
        )


class PersistentTicketButtons(PersistentViewBase):
    @discord.ui.button(
        label="Trancar",
        style=discord.ButtonStyle.green,
        custom_id="close_ticket",
        emoji="🔒",
    )
    async def close_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        ticket_owner_id = int(interaction.channel.name.split("-")[-1])
        ticket_owner = None

        while ticket_owner is None:
            try:
                ticket_owner = await interaction.guild.fetch_member(ticket_owner_id)
            except discord.HTTPException as e:
                if e.status == 429:
                    await sleep(5)
                else:
                    raise

        is_staff = is_user_staff(interaction.user.roles)
        if is_staff or interaction.user.id == ticket_owner.id:
            perms = interaction.channel.overwrites_for(ticket_owner)
            perms.send_messages = False
            await interaction.channel.set_permissions(
                ticket_owner,
                overwrite=perms,
            )

            embed = Embed(
                title="Ticket trancado!",
                description=f"{interaction.user.mention}, o ticket foi trancado, caso queira abrir novamente clique no botão destrancar.",
                color=0x9F6CFD,
            )
            await interaction.message.edit(
                view=PersistentTicketButtons().disable_buttons()
            )
            return await interaction.response.send_message(
                embed=embed, view=PersistentTicketClosedButtons()
            )

        await interaction.response.send_message(
            f"{interaction.user.mention} | Você não tem permissão para trancar o ticket!",
            ephemeral=True,
        )

    @discord.ui.button(
        label="Apagar",
        style=discord.ButtonStyle.danger,
        custom_id="delete_ticket",
        emoji="🗑️",
    )
    async def delete_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        is_staff = is_user_staff(interaction.user.roles)
        if is_staff:
            embed = Embed(
                title="O Ticket foi apagado!",
                description=f"{interaction.user.mention}, o ticket será apagado em 5 segundos!",
                color=0x9F6CFD,
            )
            await interaction.response.send_message(embed=embed)
            await interaction.message.edit(
                view=PersistentTicketButtons().disable_buttons()
            )
            await sleep(5)
            return await interaction.channel.delete()

        await interaction.response.send_message(
            f"{interaction.user.mention} | Você não tem permissão para apagar o ticket!",
            ephemeral=True,
        )


class PersistentTicketClosedButtons(PersistentViewBase):
    @discord.ui.button(
        label="Destrancar",
        style=discord.ButtonStyle.primary,
        custom_id="unclose_ticket",
        emoji="🔓",
    )
    async def unclose_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        ticket_owner_id = int(interaction.channel.name.split("-")[-1])
        ticket_owner = None

        while ticket_owner is None:
            try:
                ticket_owner = await interaction.guild.fetch_member(ticket_owner_id)
            except discord.HTTPException as e:
                if e.status == 429:
                    await sleep(5)
                else:
                    raise

        is_staff = is_user_staff(interaction.user.roles)
        if is_staff or interaction.user.id == ticket_owner.id:
            perms = interaction.channel.overwrites_for(ticket_owner)
            perms.send_messages = True
            await interaction.channel.set_permissions(
                ticket_owner,
                overwrite=perms,
            )

            embed = Embed(
                title="Ticket destrancado!",
                description=f"{interaction.user.mention}, o ticket foi destrancado, caso queira abrir tranca-lo clique no botão trancar.",
                color=0x9F6CFD,
            )
            await interaction.message.edit(
                view=PersistentTicketClosedButtons().disable_buttons()
            )
            return await interaction.response.send_message(
                embed=embed, view=PersistentTicketButtons()
            )

        await interaction.response.send_message(
            f"{interaction.user.mention} | Você não tem permissão para destrancado o ticket!",
            ephemeral=True,
        )

    @discord.ui.button(
        label="Apagar",
        style=discord.ButtonStyle.danger,
        custom_id="delete_ticket",
        emoji="🗑️",
    )
    async def delete_ticket(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        is_staff = is_user_staff(interaction.user.roles)
        if is_staff:
            embed = Embed(
                title="O Ticket foi apagado!",
                description=f"{interaction.user.mention}, o ticket será apagado em 5 segundos!",
                color=0x9F6CFD,
            )
            await interaction.response.send_message(embed=embed)
            await sleep(5)
            return await interaction.channel.delete()

        await interaction.response.send_message(
            f"{interaction.user.mention} | Você não tem permissão para apagar o ticket!",
            ephemeral=True,
        )
