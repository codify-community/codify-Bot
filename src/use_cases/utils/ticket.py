from use_cases.base import UseCase
from utils.embed import create_ticket_embed
from utils.factories import PersistentTicketView


class TicketUseCase(UseCase):

    async def execute(self):
        await self.send_message(
            embed=create_ticket_embed(), view=PersistentTicketView()
        )
