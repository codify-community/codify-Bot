from datetime import datetime, timedelta
from typing import Tuple

from env import config


def is_user_staff(roles):
    return any([role.id in config["guild"]["roles"]["staff"] for role in roles])


def is_giveaway(client, giveaway) -> bool:
    if not giveaway:
        raise ValueError("Sorteio não encontrado.")

    reaction = filter(lambda r: r.emoji == "🎉", giveaway.reactions)
    if not reaction and not client in reaction.users():
        raise ValueError("A mensagem não é um sorteio.")


def convert_to_seconds(
    time_string: str,
) -> Tuple[int, int, timedelta]:
    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    seconds = 0
    current_number = ""

    for char in time_string:
        if char.isdigit():
            current_number += char
        elif char in time_dict:
            seconds += int(current_number) * time_dict[char]
            current_number = ""
        else:
            raise ValueError(f"Caractere inválido: {char}")

    seconds_timedelta = timedelta(seconds=seconds)
    end_date = int((datetime.now() + seconds_timedelta).timestamp())

    return end_date, seconds, seconds_timedelta
