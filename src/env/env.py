from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
import os, json

load_dotenv()


class EnvSchema(BaseModel):
    python_env: str = "prod"
    mongo_uri: str
    token: str


try:
    env = EnvSchema(
        python_env=os.getenv("PYTHON_ENV"),
        mongo_uri=os.getenv("MONGO_URI"),
        token=os.getenv("TOKEN"),
    )
except ValidationError as e:
    raise Exception(f"Invalid environment variables: {e}")

with open("./src/env/config.json", "r") as f:
    config = json.load(f)[env.python_env]
