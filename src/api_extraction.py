import json
import sqlite3
from spotipy import Spotify, SpotifyClientCredentials
import time
from dotenv import dotenv_values


FILE_PREFIX = "./apidata/tracknumber_{0}.json"
number = 41

connector = sqlite3.connect("./sqldb/tracks.db")
cursor = connector.cursor()
config = dotenv_values(".env")
sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=config["CLIENT_ID"], client_secret=config["CLIENT_SECRET"]))

cursor.execute("SELECT * FROM tracks")
sqldata = cursor.fetchall()

data = {}
data["tracks"] = []
for x in range(1470000, len(sqldata), 100):
    
    track_ids = [y[0] for y in sqldata[x:x+100]]
    tracks = sp.audio_features(track_ids)
        
    for xx,y in zip(sqldata[x:x+100], tracks):
        a = {}
        a["track_uri"] = xx[0]
        a["track_name"] = xx[1]
        a["artist_name"] = xx[2]
        a["artist_uri"] = xx[3]
        a["album_name"] = xx[4]
        a["album_uri"] = xx[5]
        a["duration_ms"] = xx[6]
        a["featuers"] = y
        data["tracks"].append(a)
    
    if len(data["tracks"]) >= 35_000:
        with open(FILE_PREFIX.format(number), "w", encoding="utf-8") as file:
            json.dump(data, file , indent=4)
        data = {}
        data["tracks"] = []
        number += 1
    
    time.sleep(0.5)
    print(x)
    # 797657
        
