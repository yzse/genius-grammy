import string
from langdetect import detect
import lyricsgenius
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
from adjustText import adjust_text
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def get_lyrics_from_dataframe(df, access_token, timeout=40):
    # Initialize Genius API client with timeout
    genius = lyricsgenius.Genius(access_token, timeout=timeout)

    # Iterate over rows in dataframe
    lyrics = []
    song_names = []
    for index, row in df.iterrows():
        song_title = row['title']
        song = genius.search_song(song_title)
        if song is not None:
            song_lyrics = song.lyrics
            lyrics.append(song_lyrics)
            song_names.append(song_title)

    # Create dataframe with lyrics
    lyrics_df = pd.DataFrame(data=lyrics, index=song_names, columns=['lyrics'])
    merged_df = pd.merge(df, lyrics_df, left_on='title', right_index=True, how='left')
    merged_df.to_csv('genius_grammy.csv', index=False)
    return merged_df