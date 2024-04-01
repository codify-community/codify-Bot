from random import random
from datetime import datetime
from asyncio import sleep
from discord import TextChannel

from use_cases.base import UseCase
from utils.embed import create_giveaway_embed, create_giveaway_winners_embed
from utils.utils import convert_to_seconds, is_giveaway


class GiveawayUseCase(UseCase):

    async def execute(
        self,
        channel: TextChannel,
        name: str,
        time: str,
        description: str,
        requirements: str,
        winners: int,
        image: str,
        client,
    ):
        try:
            end_datetime, seconds, _ = convert_to_seconds(time)
        except ValueError as e:
            return await self.send_message(
                f"{self.author.mention} | O tempo inserido é inválido. {e}",
                ephemeral=self.ephemeral,
            )

        if winners < 1:
            return await self.send_message(
                f"{self.author.mention} | O número de vencedores deve ser maior que 0.",
                ephemeral=self.ephemeral,
            )

        if winners > 10:
            return await self.send_message(
                f"{self.author.mention} | O número de vencedores deve ser menor que 10.",
                ephemeral=self.ephemeral,
            )

        embed = create_giveaway_embed(
            self.author,
            name,
            description,
            requirements,
            winners,
            end_datetime,
            image,
        )

        message = await channel.send(embed=embed)
        await message.add_reaction("🎉")

        await self.send_message(
            f"{self.author.mention} | Sorteio iniciado com sucesso!",
            ephemeral=self.ephemeral,
        )

        await sleep(seconds)

        message = await channel.fetch_message(message.id)
        if not message or message.edited_at:
            return

        reactions = [
            user async for user in message.reactions[0].users() if user != client.user
        ]
        winners = sorted(reactions, key=lambda _: 0.5 - random())[0:winners]

        embed = create_giveaway_winners_embed(message, name, winners)
        await channel.send(
            (
                f"🎉 Parabéns {', '.join([winner.mention for winner in winners])}!"
                if winners
                else ""
            ),
            embed=embed,
        )


class RerollUseCase(UseCase):

    async def execute(
        self, channel: TextChannel, giveaway_id: int, new_winners: int, client
    ):
        if new_winners is not None and new_winners < 1:
            return await self.send_message(
                f"{self.author.mention} | O número de vencedores deve ser maior que 0.",
                ephemeral=self.ephemeral,
            )

        if new_winners is not None and new_winners > 10:
            return await self.send_message(
                f"{self.author.mention} | O número de vencedores deve ser menor que 10.",
                ephemeral=self.ephemeral,
            )

        giveaway = await channel.fetch_message(giveaway_id)

        try:
            is_giveaway(client, giveaway)
        except ValueError as e:
            return await self.send_message(
                f"{self.author.mention} | {e}",
                ephemeral=self.ephemeral,
            )

        giveaway_embed = giveaway.embeds[0]
        name = giveaway_embed.title
        num_winners = (
            int(giveaway_embed.fields[0].name.split(": ")[1])
            if not new_winners
            else new_winners
        )
        endtime = int(
            giveaway_embed.description.split("Sorteio encerrado ")[-1].split(":")[1]
        )

        if endtime > int(datetime.now().timestamp()):
            return await self.send_message(
                f"{self.author.mention} | O sorteio ainda não foi encerrado.",
                ephemeral=self.ephemeral,
            )

        reactions = [
            user async for user in giveaway.reactions[0].users() if user != client.user
        ]

        winners = sorted(reactions, key=lambda _: 0.5 - random())[0:num_winners]

        embed = create_giveaway_winners_embed(giveaway, name, winners)
        await self.send_message(
            (
                f"🎉 Parabéns {', '.join([winner.mention for winner in winners])}!"
                if winners
                else ""
            ),
            embed=embed,
        )


class EndUseCase(UseCase):

    async def execute(self, channel: TextChannel, giveaway_id: int, client):
        giveaway = await channel.fetch_message(giveaway_id)

        try:
            is_giveaway(client, giveaway)
        except ValueError as e:
            return await self.send_message(
                f"{self.author.mention} | {e}",
                ephemeral=self.ephemeral,
            )

        giveaway_embed = giveaway.embeds[0]
        name = giveaway_embed.title
        num_winners = int(giveaway_embed.fields[0].name.split(": ")[1])
        endtime = int(
            giveaway_embed.description.split("Sorteio encerrado ")[-1].split(":")[1]
        )

        if endtime <= int(datetime.now().timestamp()):
            return await self.send_message(
                f"{self.author.mention} | O sorteio já foi encerrado.",
                ephemeral=self.ephemeral,
            )

        reactions = [
            user async for user in giveaway.reactions[0].users() if user != client.user
        ]

        winners = sorted(reactions, key=lambda _: 0.5 - random())[0:num_winners]

        giveaway_embed.description = giveaway_embed.description.replace(
            f"{endtime}", f"{int(datetime.now().timestamp())}"
        )
        await giveaway.edit(embed=giveaway_embed)

        embed = create_giveaway_winners_embed(giveaway, name, reactions)
        await self.send_message(
            (
                f"🎉 Parabéns {', '.join([winner.mention for winner in winners])}!"
                if winners
                else ""
            ),
            embed=embed,
        )
