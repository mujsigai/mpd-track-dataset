# Unique per json

import json
import os

total_unique = 0

for x in os.listdir("./data"):
    data = []
    s = set()
    with open("./data/" + x, "r", encoding="utf-8") as file:
        jsondump = json.load(file)
        playlists = jsondump["playlists"]
        for y in playlists:
            for z in y["tracks"]:
                if z["track_uri"] in s:
                    pass
                else:
                    s.add(z["track_uri"])
                    data.append(z)
    
    with open("./extracted/" + x, "w", encoding="utf-8") as file:
        json.dump({"tracks": data}, file, indent=4)
    
    print("total", len(data))