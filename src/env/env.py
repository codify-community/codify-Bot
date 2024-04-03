from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
import os, json

load_dotenv()


class EnvSchema(BaseModel):
    environment: str
    mongo_uri: str
    token: str


try:
    env = EnvSchema(
        environment=os.getenv("ENVIRONMENT"),
        mongo_uri=os.getenv("MONGO_URI"),
        token=os.getenv("TOKEN"),
    )
except ValidationError as e:
    raise Exception(f"Invalid environment variables: {e}")

with open("./config.json", "r") as f:
    config = json.load(f)
