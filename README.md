# MPD TRACK DATASET 🎵
Extracted all unique tracks from **Million Playlist Dataset** and added audio features to every track using Spotify API.

`Total Unique Songs: 2,261,644`

## Useage of dataset
The dataset is in the form of SQL table. You can find the data on kaggle [here](https://www.kaggle.com/datasets/krishsharma0413/2-million-songs-from-mpd-with-audio-features/). Use this while respecting Spotify's Policies. We are not responsible for anything done by you using this dataset.

## Replicate the extraction
1. Install the Million Playlist Dataset from [here](https://www.kaggle.com/datasets/himanshuwagh/spotify-million).
2. Copy the `data` folder into the root project folder.
3. Run `per_json.py` -> `sql_data.py` -> `easy_extraction.py`.
4. The last step will take weeks due to rate limits by spotify.

## Future plans
Million Playlist Dataset only has songs till 2018. We plan on looking for more songs from 2018 to 2024.