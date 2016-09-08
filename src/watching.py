from pymongo import MongoClient

client = MongoClient()
db = client.twitch_01

result = db.usersWatching.insert_one(
    {
        "streamname": "mroseman_bot",
        "watching": ["stream1", "stream2"]
    }
)

print (result.inserted_id)
