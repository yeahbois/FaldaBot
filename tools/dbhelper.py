import pymongo
import os
import dotenv

dotenv.load_dotenv()

# Connect to the mongodb || get the key and client
key = os.getenv("databaseurl")
client = pymongo.MongoClient(key)

# All the database
db = client['allaybot']
db_eco = client['allaybot-economy']

# All the collection
col_setting = db['setting']
col_guilds = db['guilds']
col_users = db['users']
col_music = db['music']
col_money = db_eco['user-money']
col_profile = db_eco['user-profile']
col_cd = db_eco['user-cooldowns']
col_clans = db_eco['clans']