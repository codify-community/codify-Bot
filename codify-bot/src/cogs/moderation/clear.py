from discord.ext import commands
from discord import app_commands, Interaction, Client
from discord.ext.commands import Context

from use_cases.moderation.clear import ClearUseCase


class ClearCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.command(name="limpar", aliases=["clear"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: Context, quantidade: int = 5):
        clear_use_case = ClearUseCase(send=ctx.send, author=ctx.author)
        await clear_use_case.execute(ctx.channel, quantidade)

    @app_commands.command(
        name="limpar",
        description="Limpa o chat.",
    )
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear_slash(self, interaction: Interaction, quantidade: int = 5):
        clear_use_case = ClearUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await clear_use_case.execute(
            interaction.channel, quantidade, interaction.response
        )


async def setup(client):
    await client.add_cog(ClearCog(client))
