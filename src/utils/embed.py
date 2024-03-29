from discord import Embed

from env import config


def create_giveaway_winners_embed(message, name, winners):
    embed = Embed(
        title=name,
        description=(
            f"Parabéns ao(s) vencedor(es) de [{name}]({message.jump_url})!\n{', '.join([winner.mention for winner in winners])} 🎉"
            if winners
            else f"[{name}]({message.jump_url}) não teve nenhum ganhador! É sua chance de ganhar na próxima!"
        ),
        color=0xFF3030,
    )
    embed.set_thumbnail(url=config["guild"]["icon"])
    embed.set_footer(text=f"ID do sorteio: {message.id}")

    return embed


def create_giveaway_embed(
    member, name, description, requirements, winners, endtime, image
):
    embed = Embed(
        title=name,
        description=f"{description}\nSorteio encerrado <t:{endtime}:R>.",
        color=0xFF3030,
    )

    embed.set_thumbnail(url=config["guild"]["icon"])

    if requirements:
        embed.add_field(name="Requisitos", value=f"> {requirements}", inline=False)
    embed.add_field(name=f"Número de vencedores: {winners}", value="", inline=False)
    embed.set_footer(text="Reaja com 🎉 para participar!")
    embed.set_author(name=member.display_name, icon_url=member.avatar.url)

    if image:
        embed.set_image(url=image)

    return embed


def create_ticket_embed():
    embed = Embed(
        color=0xFF3030,
        title="Atendimento - NRRP",
        description="Olá, bem vindo a Central de Atendimento do Nex Revolution - RP. Eu sou responsável por facilitar a sua comunicação com a administração de um jeito prático e rápido.",
    )
    embed.set_footer(text="Adiministração Nex Revolution")
    embed.set_image(url=config["guild"]["icon"])

    return embed


def create_warns_embed(member, warns, page: int):
    embed = Embed(
        title=f"Warns de {member.name.capitalize()}",
        description="",
        color=0xFF3030,
    )
    embed.set_thumbnail(url=member.avatar.url)
    for warn in warns["results"]:
        embed.add_field(
            name=f"{warn['id']}",
            value=f"Motivo: {warn['reason']}\nData: {warn['creation_date']}",
            inline=False,
        )
    embed.set_footer(
        text=f"Página {page}/{warns['count']//5 + 1} Total de warns: {warns['count']}"
    )
    return embed


def create_lock_embed(locked: bool = False):
    if locked:
        embed = Embed(
            title="Canal trancado",
            description="Este canal foi trancado!",
            color=0xFF3030,
        )
        embed.set_thumbnail(
            url="https://www.dropbox.com/scl/fi/lzziw2iouwz8m3gu6mq5f/fechadura.png?rlkey=jwe7616xfuez158tkjk213tbc&raw=1"
        )
        embed.set_footer(text="Nenhum membro poderá enviar mensagens neste canal.")
    else:
        embed = Embed(
            title="Canal destrancado",
            description="Este canal foi destrancado!",
            color=0x00FF84,
        )
        embed.set_thumbnail(
            url="https://www.dropbox.com/scl/fi/lwgivus2ker2o9m8gxm80/desbloquear.png?rlkey=wr4to01y1j3iq1tfr8jkcg0bh&raw=1"
        )
        embed.set_footer(text="Membros poderão enviar mensagens neste canal.")

    return embed
