from discord.ext.commands import Context
from discord.ext import commands
from discord import Interaction, app_commands

from use_cases.general.translate import (
    TranslateMessageUseCase,
    TranslateUseCase,
    linguagens,
)


escolhas = [
    app_commands.Choice(name=f"{linguagem} ({codigo})", value=codigo)
    for linguagem, codigo in linguagens.items()
]


class TranslateCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="translate text", aliases=["traduzir texto", "tt"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def translate(
        self, ctx: Context, from_lang: str, to_lang: str, *, text: str = None
    ):
        translate_use_case = TranslateUseCase(
            send=ctx.send,
            author=ctx.author,
        )
        await translate_use_case.execute(
            de=from_lang,
            para=to_lang,
            texto=text,
        )

    group = app_commands.Group(name="traduzir", description="Comandos de tradução.")

    @group.command(name="texto", description="Traduz um texto.")
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.choices(
        de=[app_commands.Choice(name="Detectar (auto)", value="auto")] + escolhas,
        para=escolhas,
    )
    async def translate_slash(
        self,
        interaction: Interaction,
        texto: str,
        de: app_commands.Choice[str] = None,
        para: app_commands.Choice[str] = None,
    ):
        translate_use_case = TranslateUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await translate_use_case.execute(
            de=de.value if de else "auto",
            para=para.value if para else "pt",
            texto=texto,
        )

    @commands.command(name="translate message", aliases=["traduzir mensagem", "tm"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def translate_message(
        self,
        ctx: Context,
        message: str,
        from_lang: str,
        to_lang: str,
    ):
        translate_message_use_case = TranslateMessageUseCase(
            send=ctx.send,
            author=ctx.author,
        )
        await translate_message_use_case.execute(
            message=message,
            de=from_lang,
            para=to_lang,
            channel=ctx.channel,
        )

    @group.command(name="mensagem", description="Traduz uma mensagem.")
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.choices(
        de=[app_commands.Choice(name="Detectar (auto)", value="auto")] + escolhas,
        para=escolhas,
    )
    async def translate_message_slash(
        self,
        interaction: Interaction,
        mensagem: str,
        de: app_commands.Choice[str] = None,
        para: app_commands.Choice[str] = None,
    ):
        translate_message_use_case = TranslateMessageUseCase(
            send=interaction.response.send_message,
            author=interaction.user,
            ephemeral=True,
        )
        await translate_message_use_case.execute(
            message=mensagem,
            de=de.value if de else "auto",
            para=para.value if para else "pt",
            channel=interaction.channel,
            interaction=interaction,
        )


async def setup(client):
    await client.add_cog(TranslateCog(client))
