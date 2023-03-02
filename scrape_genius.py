import lyricsgenius
import pandas as pd

def get_lyrics_from_songs(df, access_token):
    genius = lyricsgenius.Genius(access_token, remove_section_headers=True, timeout=40)
    lyrics = []
    song_names = []

    # Parse songs
    for index, row in df.iterrows():
        title = row['title']
        artist = row.get('artist')
        if pd.notna(artist):
            song = genius.search_song(title, artist)
        else:
            song = genius.search_song(title)
        if song is not None:
            song_names.append(title)
            lyrics.append(song.lyrics)

    df['lyrics'] = lyrics
    df.to_csv('genius_grammy.csv')