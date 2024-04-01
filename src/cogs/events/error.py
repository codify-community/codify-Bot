import time
from discord.ext import commands
from discord import Interaction, app_commands
from discord.app_commands import AppCommandError
from discord.ext.commands import Context, CommandError


class ErrorCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError) -> None:
        def get_error_message(error):
            if isinstance(error, commands.CommandOnCooldown):
                return f"{ctx.author.mention} | Você está em cooldown. Você pode usar comandos novamente <t:{int(time.time() + error.retry_after)}:R>."
            elif isinstance(error, commands.MissingPermissions):
                return f"{ctx.author.mention} | Você não tem permissão para usar esse comando."
            elif isinstance(error, commands.BotMissingPermissions):
                return f"{ctx.author.mention} | Eu não tenho permissão para fazer isso."
            elif isinstance(error, commands.MissingRequiredArgument):
                return f"{ctx.author.mention} | Você esqueceu de passar um argumento obrigatório."
            elif isinstance(error, commands.CommandNotFound):
                return f"{ctx.author.mention} | Esse comando não existe."

            print(f"❌ {error}")
            return f"{ctx.author.mention} | Ocorreu um erro ao executar esse comando."

        await ctx.send(get_error_message(error))

    async def cog_load(self) -> None:
        self.client.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self, interaction: Interaction, error: AppCommandError
    ) -> None:
        def get_error_message(error: AppCommandError):
            if isinstance(error, app_commands.errors.CommandOnCooldown):
                return f"{interaction.user.mention} | Você está em cooldown. Você pode usar esse comando novamente <t:{int(time.time() + error.retry_after)}:R>."
            elif isinstance(error, app_commands.errors.MissingPermissions):
                return f"{interaction.user.mention} | Você não tem permissão para usar esse comando."
            elif isinstance(error, app_commands.errors.BotMissingPermissions):
                return f"{interaction.user.mention} | Eu não tenho permissão para fazer isso."
            elif isinstance(error, app_commands.errors.CommandNotFound):
                return f"{interaction.user.mention} | Esse comando não existe."

            print(f"❌ {error}")
            return f"{interaction.user.mention} | Ocorreu um erro ao executar esse comando."

        await interaction.response.send_message(
            get_error_message(error), ephemeral=True
        )


async def setup(client):
    await client.add_cog(ErrorCog(client))
