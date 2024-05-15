from discord.ext.commands import Context
from discord.ext import commands
from discord import app_commands, Interaction, Client

from use_cases.general.top_bumpers import TopBumpersUseCase
from env import config


class TopBumpersCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="topbumpers", aliases=["tb"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def top_bumpers(self, ctx: Context):
        top_bumpers_use_case = TopBumpersUseCase(send=ctx.send, author=ctx.author)
        await top_bumpers_use_case.execute(
            guild=ctx.guild,
            client=self.client,
        )

    group = app_commands.Group(name="top", description="...")

    @group.command(name="bumpers", description="Mostra os top bumpers do servidor.")
    @app_commands.checks.cooldown(1, 10, key=lambda i: i.user.id)
    async def top_bumpers_slash(self, interaction: Interaction):
        top_bumpers_use_case = TopBumpersUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await top_bumpers_use_case.execute(guild=interaction.guild, client=self.client)


async def setup(client):
    await client.add_cog(TopBumpersCog(client))
