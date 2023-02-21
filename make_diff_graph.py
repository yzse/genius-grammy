#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%%
def make_diff_graph(df):
# read data and filter outliers
    mean_gloom = df['gloom_index'].mean()
    std_gloom = df['gloom_index'].std()
    df = df[(df['gloom_index'] > mean_gloom - 4 * std_gloom) & (df['gloom_index'] < mean_gloom + 4 * std_gloom)]

    # group data by award status and create scatter plot
    grouped = df.groupby('winner')['gloom_index']
    fig, ax = plt.subplots(figsize=(6,6))
    nominee_plot = ax.scatter([0]*len(grouped.get_group(0)), grouped.get_group(0), s=80, alpha=0.4, label='Nominee')
    winner_plot = ax.scatter([1]*len(grouped.get_group(1)), grouped.get_group(1), s=80, alpha=0.4, label='Winner')

    # add mean + line between means
    ax.scatter(0, grouped.get_group(0).mean(), c='black', s=80)
    ax.scatter(1, grouped.get_group(1).mean(), c='black', s=80)
    ax.plot([0, 1], [grouped.get_group(0).mean(), grouped.get_group(1).mean()], c='black', linestyle='--')

    # set axis ticks and labels
    ax.set_xticks([0, 1])
    ax.set_xlabel('Award Status')
    ax.set_ylabel('Gloom Index')
    ax.set_title('Gloom Index by Award Status')

    # plot styling
    ax.set_axisbelow(True)
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax.set_xticks([-0.75,1.75])
    ax.tick_params(axis='y', which='both', labelsize='15')
    ax.set_yticks(np.arange(0, 100, 10))
    ax.legend(handles=[nominee_plot, winner_plot], scatterpoints=1, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, fontsize=16)
    ax.set_title('Gloom Index by Award Status', fontsize=22)
    ax.set_xlabel('Award Status', fontsize=17)
    ax.set_ylabel('Gloom Index', fontsize=17)
    ax.grid()

    fig.set_size_inches(10, 20)
    fig.subplots_adjust(wspace=0.2)

    # save and show plot
    plt.savefig("gloom_index_mean_diff.png")
    plt.show()

    return plt
#%%