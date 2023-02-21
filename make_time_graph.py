#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%
# read data and filter outliers
def make_time_graph(df):
    mean_gloom = df['gloom_index'].mean()
    std_gloom = df['gloom_index'].std()
    df = df[(df['gloom_index'] > mean_gloom - 4 * std_gloom) & (df['gloom_index'] < mean_gloom + 4 * std_gloom)]

    sns.set_style('whitegrid')
    sns.lmplot(x='year', y='gloom_index', hue='winner', data=df, scatter_kws={"alpha":0.5},
            height=5, aspect=1.5, legend=False);
    plt.legend(title='Status', labels=['Nominee', 'Winner'], loc='upper right')
    plt.title('Gloom Index by Year and Winner')
    plt.xlabel('Year')
    plt.ylabel('Gloom Index')

    plt.savefig('gloom_index_time_series.jpeg', dpi=300, bbox_inches='tight')

    return plt