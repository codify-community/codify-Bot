from datetime import datetime, timedelta
from typing import Tuple, Literal

from discord import Role, User

from env import config


def create_message(
    type: Literal["success", "error", "cooldown"] = "success",
    message: str = "",
    author: User = None,
):
    return f"{'✅ ' if type == 'success' else '❌ ' if type == 'error' else '⏳ '}{f'{author.mention} ' if author else ''}**|** {message}"


def create_user_json(user: User, role: Role):
    return {
        "id": user.id,
        "role": config["guild"]["roles_name"][str(role.id)],
        "name": user.name,
        "avatarUrl": str(user.avatar.url),
    }


def get_updated_users(discord_users, db_users):
    updated_users = []

    for user in discord_users:
        db_user = {}

        for i in db_users:
            if user["id"] == i["member"]["id"]:
                db_user = i
                break

        if db_user:
            db_user.update(user)
            updated_users.append(db_user)
        else:
            updated_users.append(
                {
                    "role": user["role"],
                    "member": {
                        "id": user["id"],
                        "name": user["name"],
                        "avatarUrl": user["avatarUrl"],
                    },
                }
            )

    return updated_users


def is_user_staff(roles):
    return any(
        [
            role.id
            in config["guild"]["roles"]["staff"] + config["guild"]["roles"]["staffs"]
            for role in roles
        ]
    )


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
