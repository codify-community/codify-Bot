from discord import app_commands, Interaction
from discord.ext.commands import Context
from discord.ext import commands

from use_cases.utils.ticket import TicketUseCase


class TicketCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.group(
    #     name="configurartickets",
    #     aliases=["setuptickets", "st"],
    #     invoke_without_command=True,
    # )
    # @commands.cooldown(1, 5, commands.BucketType.guild)
    # @commands.has_permissions(administrator=True)
    # async def setup_tickets(self, ctx: Context):
    #     ticket_use_case = TicketUseCase(send=ctx.send, author=ctx.author)
    #     await ticket_use_case.execute()

    # group = app_commands.Group(
    #     name="tickets",
    #     description="...",
    # )

    # @group.command(
    #     name="configurar",
    #     description="Envia o embed de criação de tickets.",
    # )
    # @app_commands.checks.cooldown(1, 5, key=lambda i: i.guild.id)
    # @app_commands.default_permissions(administrator=True)
    # @app_commands.checks.has_permissions(administrator=True)
    # async def setup_tickets_slash(self, interaction: Interaction):
    #     ticket_use_case = TicketUseCase(
    #         send=interaction.response.send_message,
    #         author=interaction.user,
    #         ephemeral=True,
    #     )
    #     await ticket_use_case.execute()


async def setup(client):
    await client.add_cog(TicketCog(client))
