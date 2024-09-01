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


# extracted sql
extracted_connector = sqlite3.connect("./sqldb/extracted.db")
extracted_cursor = extracted_connector.cursor()

extracted_cursor.execute(
    "CREATE TABLE IF NOT EXISTS extracted(track_uri TEXT PRIMARY KEY, track_name TEXT, artist_name TEXT, artist_uri TEXT, album_name TEXT, album_uri TEXT, duration_ms INTEGER, danceability REAL, energy REAL, key INTEGER, loudness REAL, mode INTEGER, speechiness REAL, acousticness REAL, instrumentalness REAL, liveness REAL, valence REAL, tempo REAL, type TEXT, id TEXT, uri TEXT, track_href TEXT, analysis_url TEXT, fduration_ms INTEGER, time_signature INTEGER)" 
)

extracted_cursor.execute("SELECT * FROM extracted")
alldata = extracted_cursor.fetchall()

left = len(sqldata) - len(alldata)
print("\nhello krish!")
print("total number of tracks left for API processing are ", left)


track_ids = []
data = []
collected = {x[0] for x in alldata}

for x in sqldata[::-1]:
    if x[0] in collected:
        continue
    
    if len(data) == len(track_ids) == 100:
        tracks = sp.audio_features(track_ids)
        time.sleep(0.5)
        for xx,yy in zip(data, tracks):
            y = {}
            y["track_uri"] = xx[0]
            y["track_name"] = xx[1]
            y["artist_name"] = xx[2]
            y["artist_uri"] = xx[3]
            y["album_name"] = xx[4]
            y["album_uri"] = xx[5]
            y["duration_ms"] = xx[6]
            y["featuers"] = yy
            if yy == None:
                continue
            extracted_cursor.execute(
                "INSERT OR IGNORE INTO extracted VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (y["track_uri"], y["track_name"], y["artist_name"], y["artist_uri"], y["album_name"], y["album_uri"], y["duration_ms"],
                y["featuers"]["danceability"], y["featuers"]["energy"], y["featuers"]["key"], y["featuers"]["loudness"], y["featuers"]["mode"],
                y["featuers"]["speechiness"], y["featuers"]["acousticness"], y["featuers"]["instrumentalness"], y["featuers"]["liveness"],
                y["featuers"]["valence"], y["featuers"]["tempo"], y["featuers"]["type"], y["featuers"]["id"], y["featuers"]["uri"],
                y["featuers"]["track_href"], y["featuers"]["analysis_url"], y["featuers"]["duration_ms"], y["featuers"]["time_signature"]
                )
            )
        print("completed 100 more...")
        extracted_connector.commit()
        
        data = []
        track_ids = []
       
    else:
        data.append(x)
        track_ids.append(x[0])