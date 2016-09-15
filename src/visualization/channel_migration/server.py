from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
import pdb

app = Flask(__name__)
#  NOTE comment out on release build
app.debug = True

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'twitch_01'
COLLECTION_NAME = 'usersWatching'

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/streams/")
@app.route("/streams/<name>")
def streams_migration(name=None):
    #  NOTE comment out on release build
    #pdb.set_trace()
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DBS_NAME][COLLECTION_NAME]
    if name is not None:
        streams = collection.find({ 'streamname': name })
    else:
        streams = collection.find()
    json_streams = []
    for stream in streams:
        json_streams.append(stream)
    json_streams = json.dumps(json_streams, default=json_util.default)
    connection.close()
    return json_streams


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
