from typing import Callable, Union
from discord import User, Member


class UseCase:
    def __init__(
        self,
        send: Callable,
        author: Union[User, Member, None] = None,
        ephemeral: bool = False,
    ) -> None:
        self.send = send
        self.author = author
        self.ephemeral = ephemeral

    async def execute(self, *args, **kwargs) -> None:
        raise NotImplementedError("UseCase does't implement 'execute' method.")

    async def send_message(
        self, content: str = None, ephemeral=False, **kwargs
    ) -> None:
        await self.send(content, **({"ephemeral": True} if ephemeral else {}), **kwargs)
