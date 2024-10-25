from typing import TYPE_CHECKING
from discord import Role

if TYPE_CHECKING:
    from discord.abc import MessageableChannel

from use_cases.base import UseCase
from utils.embed import create_lock_embed


class LockUseCase(UseCase):

    async def execute(
        self, channel: "MessageableChannel", default_role: "Role"
    ) -> None:
        channel_permissions = channel.permissions_for(default_role)
        await channel.set_permissions(
            default_role,
            send_messages=True if not channel_permissions.send_messages else False,
        )

        await self.send_message(
            self.author.mention,
            embed=create_lock_embed(locked=channel_permissions.send_messages),
        )
