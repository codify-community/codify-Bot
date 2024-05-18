import re
from discord import TextChannel
from use_cases.base import UseCase

from deep_translator import GoogleTranslator as Translator


linguagens = {
    "Inglês": "en",
    "Chinês": "zh-CN",
    "Espanhol": "es",
    "Francês": "fr",
    "Árabe": "ar",
    "Russo": "ru",
    "Português": "pt",
    "Alemão": "de",
    "Japonês": "ja",
    "Turco": "tr",
    "Coreano": "ko",
    "Vietnamita": "vi",
    "Italiano": "it",
    "Polonês": "pl",
    "Latim": "la",
    "Holandês": "nl",
    "Ucraniano": "uk",
    "Filipino": "tl",
    "Albanês": "sq",
    "Grego": "el",
    "Romeno": "ro",
    "Tailandês": "th",
    "Luxemburguês": "lb",
    "Lituano": "lt",
}


class TranslateUseCase(UseCase):
    def __init__(self, send, author, ephemeral=False) -> None:
        super().__init__(send, author, ephemeral)

    async def execute(
        self,
        de: str,
        para: str,
        texto: str = None,
    ):
        if not texto:
            return await self.send_message(
                content=f"{self.author.mention} | Você precisa informar um texto para traduzir.",
                ephemeral=self.ephemeral,
            )

        if de != "auto" and de not in linguagens.values():
            return await self.send_message(
                content=f"{self.author.mention} | Linguagem de origem inválida.",
                ephemeral=self.ephemeral,
            )

        if para not in linguagens.values():
            return await self.send_message(
                content=f"{self.author.mention} | Linguagem de destino inválida.",
                ephemeral=self.ephemeral,
            )

        try:
            translator = Translator(source=de, target=para)
            traduzido = translator.translate(texto)
        except:
            return await self.send_message(
                content=f"{self.author.mention} | Erro ao traduzir o texto. Consulte um administrador.",
                ephemeral=self.ephemeral,
            )

        await self.send_message(content=traduzido)


class TranslateMessageUseCase(UseCase):
    def __init__(self, send, author, ephemeral=False) -> None:
        super().__init__(send, author, ephemeral)

    async def execute(
        self,
        message: str,
        de: str,
        para: str,
        channel: TextChannel,
        interaction=None,
    ):
        try:
            message = await channel.fetch_message(message)
        except:
            return await self.send_message(
                content=f"{self.author.mention} | Mensagem não encontrada.",
                ephemeral=self.ephemeral,
            )

        text = message.content
        clean_text = re.sub(r"<@!?\d+>", "", text)

        if not clean_text:
            return await self.send_message(
                content=f"{self.author.mention} | Você precisa informar um texto para traduzir.",
                ephemeral=self.ephemeral,
            )

        if de != "auto" and de not in linguagens.values():
            return await self.send_message(
                content=f"{self.author.mention} | Linguagem de origem inválida.",
                ephemeral=self.ephemeral,
            )

        if para not in linguagens.values():
            return await self.send_message(
                content=f"{self.author.mention} | Linguagem de destino inválida.",
                ephemeral=self.ephemeral,
            )

        try:
            translator = Translator(source=de, target=para)
            traduzido = translator.translate(clean_text)
        except:
            return await self.send_message(
                content=f"{self.author.mention} | Erro ao traduzir o texto. Consulte um administrador.",
                ephemeral=self.ephemeral,
            )

        await channel.send(reference=message, content=traduzido)
        if interaction:
            await interaction.response.send_message(
                content=f"{self.author.mention} | Mensagem traduzida com sucesso.",
                ephemeral=self.ephemeral,
            )
