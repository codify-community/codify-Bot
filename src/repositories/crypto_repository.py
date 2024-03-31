from typing import Dict
from datetime import datetime

from .connection import client


class CryptoRepository:
    def __init__(self) -> None:
        self.collection = client["codify"]["crypto"]

    async def update_prices(self, data: Dict[str, str]) -> None:
        old_prices = self.collection.find_one({"_id": "0"})

        prices = {
            crypto["symbol"]: {
                "price": crypto["price"],
                "status": (
                    "up"
                    if old_prices
                    and old_prices["prices"][crypto["symbol"]]["price"]
                    < crypto["price"]
                    else "down"
                ),
            }
            for crypto in data
        }

        if not old_prices:
            self.collection.insert_one(
                {"_id": "0", "prices": prices, "updatedAt": datetime.now()}
            )
            return

        self.collection.update_one(
            {"_id": "0"}, {"$set": {"prices": prices, "updatedAt": datetime.now()}}
        )


cryptoRepository = CryptoRepository()
