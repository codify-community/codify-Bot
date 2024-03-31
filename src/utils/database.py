from typing import List, Dict
from pymongo import MongoClient
from pymongo.results import InsertOneResult, UpdateResult
from uuid import uuid4
from datetime import datetime
import certifi

from env import env

ca = certifi.where()
client = MongoClient(env.mongo_uri, tlsCAFile=ca)


class UserDatabase:
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


class PropsDatabase:
    def __init__(self) -> None:
        self.collection = client["props-v2"]["info"]


class StatsDatabase:
    def __init__(self) -> None:
        self.collection = client["stats"]["general"]

    async def get_users(self) -> List[Dict[str, str]]:
        stats = self.collection.find_one({"_id": "0"})

        staffs = [
            staff for staff in stats["specialMembers"] if staff["role"] != "booster"
        ]
        boosters = [
            staff for staff in stats["specialMembers"] if staff["role"] == "booster"
        ]

        return staffs, boosters

    async def update(
        self,
        channel_count: int,
        member_count: int,
        specialMembers: List[Dict[str, str]],
    ) -> UpdateResult:
        print(channel_count)
        print(member_count)
        print(specialMembers)
        return self.collection.update_one(
            {"_id": "0"},
            {
                "$set": {
                    "channelCount": channel_count,
                    "memberCount": member_count,
                    "specialMembers": specialMembers,
                }
            },
        )


userDatabase = UserDatabase()
propsDatabase = PropsDatabase()
statsDatabase = StatsDatabase()
