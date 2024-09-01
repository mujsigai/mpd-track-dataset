import json
import os
import sqlite3

connector = sqlite3.connect("./sqldb/tracks.db")
cursor = connector.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tracks (track_uri TEXT PRIMARY KEY, track_name TEXT, artist_name TEXT, artist_uri TEXT, album_name TEXT, album_uri TEXT, duration_ms INTEGER)")

for x in os.listdir("./extracted"):
    with open("./extracted/" + x, "r", encoding="utf-8") as file:
        jsondump = json.load(file)
        for y in jsondump["tracks"]:
            cursor.execute(
                "INSERT OR IGNORE INTO tracks VALUES (?, ?, ?, ?, ?, ?, ?)",
                (y["track_uri"], y["track_name"], y["artist_name"], y["artist_uri"], y["album_name"], y["album_uri"], y["duration_ms"])
            )
    
    connector.commit()
