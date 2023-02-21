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
    genius = lyricsgenius.Genius(access_token, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True,timeout=timeout)

    # Iterate over rows in dataframe
    c = 0
    for title in df:
        try:
            songs = (genius.search_song(df))
            s = [song.lyrics for song in songs]
            lyrics_df = pd.DataFrame(data=s, index=s, columns=['lyrics'])
            merged_df = pd.merge(df, lyrics_df, left_on='title', right_index=True, how='left')
            c += 1
            print(f"Songs grabbed:{len(s)}")
        except:
            print(f"some exception at {title}: {c}")
    merged_df.to_csv('genius_grammy.csv', index=False)
    return merged_df