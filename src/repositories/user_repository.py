from uuid import uuid4
from datetime import datetime

from connection import client


class UserRepository:
    def __init__(self):
        self.collection = client["codify"]["users"]

    async def create_user(self, user_id: int) -> dict:
        user = {
            "_id": user_id,
            "warns": [],
        }
        self.collection.insert_one(user)
        return user

    async def get_user(self, user_id) -> dict:
        user = self.collection.find_one({"_id": user_id})
        if not user:
            return await self.create_user(user_id)

        return user

    async def get_warns(self, user_id: int, page_size: int = 5, page: int = 1) -> dict:
        user = await self.get_user(user_id)
        warns = user["warns"][::-1]
        paginated_warns = warns[(page - 1) * page_size : page * page_size]
        return {"results": paginated_warns, "count": len(warns)}

    async def add_warn(self, user_id: int, reason: str) -> None:
        warn = {
            "reason": reason if reason else "Sem motivo.",
            "creation_date": datetime.now().strftime("%d/%m/%Y as %H:%M"),
            "id": str(uuid4()),
        }

        self.collection.update_one({"_id": user_id}, {"$push": {"warns": warn}})

    async def remove_warn(self, user_id: int, warn_id: str) -> None:
        if not self.collection.count_documents({"_id": user_id, "warns.id": warn_id}):
            raise ValueError("Warn not found.")

        self.collection.update_one(
            {"_id": user_id},
            {"$pull": {"warns": {"id": warn_id}}},
        )


userRepository = UserRepository()
