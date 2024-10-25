from pymongo import MongoClient
import certifi

from env import env

ca = certifi.where()
client = MongoClient(env.mongo_uri, tlsCAFile=ca)
