from discord.ext import commands
from discord import app_commands, Member, Interaction
from discord.ext.commands import Context

from use_cases.general.npap import NpapUseCase


class NpapCog(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @commands.command("naopergunteparapeguntar", aliases=["dafa", "npap"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def npap(self, ctx: Context, membro: Member):
        npap_use_case = NpapUseCase(send=ctx.send, author=ctx.author)
        await npap_use_case.execute(membro)

    @app_commands.command(
        name="npap",
        description="Não pergunte para perguntar.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    async def npap_slash(self, interaction: Interaction, membro: Member):
        npap_use_case = NpapUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await npap_use_case.execute(membro)


async def setup(client):
    await client.add_cog(NpapCog(client))
