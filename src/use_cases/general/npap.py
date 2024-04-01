from discord import Embed, Member

from use_cases.base import UseCase

from env import config


class NpapUseCase(UseCase):

    async def execute(
        self,
        member: Member,
    ) -> None:
        if member.bot:
            return await self.send_message(
                f"{self.author.mention} | Você não pode usar esse comando em bots.",
                ephemeral=self.ephemeral,
            )

        if self.author == member:
            return await self.send_message(
                f"{self.author.mention} | Você não pode usar esse comando em si mesmo.",
                ephemeral=self.ephemeral,
            )

        embed = Embed(
            title="Não pergunte para perguntar",
            description=f"""{member.display_name}, você não precisa perguntar para perguntar.

Em vez disso, envie sua dúvida de forma clara, detalhada e objetiva.
Assim você se ajuda a ser ajudado.

Exemplos:

❌Errado
Alguém consegue me tirar uma dúvida?

✅ Certo
Envie sua duvida no fórum <#1091053478157230120> (ou em algum forúm na categoria da sua duvida) com as devidas tags.

> Preciso listar todos os itens de um array, mas não estou sabendo como.
> O que já fiz: https://www.online-python.com/example
> Alguém saberia como?

Para enviar código, envie lá.
Para enviar imagens/arquivos, envie lá.""",
            color=0x9F6CFD,
        )
        embed.set_thumbnail(url=config["guild"]["icon"])

        await self.send_message(member.mention, embed=embed)
