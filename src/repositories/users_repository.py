from uuid import uuid4
from datetime import datetime

from .connection import client


class UsersRepository:
    def __init__(self):
        self.collection = client["codify"]["users"]

    async def create(self, user_id: int) -> dict:
        return self.collection.insert_one(
            {
                "_id": user_id,
                "money": 0.0,
                "wallet": {},
                "warns": [],
                "bumpCount": 0,
            }
        )

    async def get_user(self, user_id) -> dict:
        user = self.collection.find_one({"_id": user_id})
        if not user:
            return await self.create(user_id)

        return user

    async def fetch_warns(
        self, user_id: int, page_size: int = 5, page: int = 1
    ) -> dict:
        user = await self.get_user(user_id)
        warns = user["warns"][::-1]
        paginated_warns = warns[(page - 1) * page_size : page * page_size]

        return {"results": paginated_warns, "count": len(warns)}

    async def create_warn(self, user_id: int, reason: str) -> None:
        await self.get_user(user_id)
        self.collection.update_one(
            {"_id": user_id},
            {
                "$push": {
                    "warns": {
                        "reason": reason if reason else "Sem motivo.",
                        "creation_date": datetime.now().strftime("%d/%m/%Y as %H:%M"),
                        "id": str(uuid4()),
                    }
                }
            },
        )

    async def remove_warn(self, user_id: int, warn_id: str) -> None:
        await self.get_user(user_id)
        if not self.collection.count_documents({"_id": user_id, "warns.id": warn_id}):
            raise ValueError("Warn not found.")

        self.collection.update_one(
            {"_id": user_id},
            {"$pull": {"warns": {"id": warn_id}}},
        )

    async def bump(self, user_id: int) -> None:
        await self.get_user(user_id)
        self.collection.update_one({"_id": user_id}, {"$inc": {"bumpCount": 1}})


users_repository = UsersRepository()
