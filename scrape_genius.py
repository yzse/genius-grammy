import lyricsgenius
import pandas 

def get_lyrics(df, artist_column, song_column, access_token):
    genius = lyricsgenius.Genius(access_token, remove_section_headers=True, timeout=40)
    df['song_lyrics'] = None
    not_found = []
    for i, row in df.iterrows():
        try:
            song = genius.search_song(row[song_column], row[artist_column])
            lyrics = song.lyrics
            df.at[i, 'song_lyrics'] = lyrics
        except:
            not_found.append(f'{row[artist_column]} - {row[song_column]}')
            df.at[i, 'song_lyrics'] = None
        finally:
            pass
    df['song_lyrics'] = df['song_lyrics'].str.replace('\n', ' ')
    df.to_csv('genius_grammy.csv', index=False)