import time
from discord.ext import commands
from discord import Client, Interaction, app_commands
from discord.app_commands import AppCommandError
from discord.ext.commands import Context, CommandError


class ErrorEventCog(commands.Cog):
    def __init__(self, client: Client) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError) -> None:
        def get_error(error):
            if isinstance(error, commands.CommandOnCooldown):
                return (
                    "cooldown",
                    f"Você está em cooldown. Você pode usar comandos novamente <t:{int(time.time() + error.retry_after)}:R>.",
                )
            elif isinstance(error, commands.MissingPermissions):
                return (
                    "error",
                    "Você não tem permissão para usar esse comando.",
                )
            elif isinstance(error, commands.BotMissingPermissions):
                return (
                    "error",
                    "Eu não tenho permissão para fazer isso.",
                )
            elif isinstance(error, commands.MissingRequiredArgument):
                return (
                    "error",
                    "Você esqueceu de passar um argumento obrigatório.",
                )
            elif isinstance(error, commands.CommandNotFound):
                return (
                    "error",
                    "Esse comando não existe.",
                )

            print(f"❌ {error}")
            return ("error" "Ocorreu um erro ao executar esse comando.",)

        error_type, error = get_error(error)
        await ctx.send(
            f"{'❌' if error_type == 'error' else '⏳'} {ctx.author.mention} | {error}"
        )

    async def cog_load(self) -> None:
        self.client.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self, interaction: Interaction, error: AppCommandError
    ) -> None:
        def get_error(error: AppCommandError):
            if isinstance(error, app_commands.errors.CommandOnCooldown):
                return (
                    "cooldown",
                    f"Você está em cooldown. Você pode usar esse comando novamente <t:{int(time.time() + error.retry_after)}:R>.",
                )
            elif isinstance(error, app_commands.errors.MissingPermissions):
                return (
                    "error",
                    "Você não tem permissão para usar esse comando.",
                )
            elif isinstance(error, app_commands.errors.BotMissingPermissions):
                return (
                    "error",
                    "Eu não tenho permissão para fazer isso.",
                )
            elif isinstance(error, app_commands.errors.CommandNotFound):
                return "error", "Esse comando não existe."

            print(f"❌ {error}")
            return "error", "Ocorreu um erro ao executar esse comando."

        error_type, error = get_error(error)
        await interaction.response.send_message(
            f"{'❌' if error_type == 'error' else '⏳'} {interaction.user.mention} | {error}",
            ephemeral=True,
        )


async def setup(client):
    await client.add_cog(ErrorEventCog(client))
