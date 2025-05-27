import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def make_plot(path):
    df = pd.read_csv(path)
    scores = np.array(df.Scores)

    plt.figure(figsize=(720/100, 500/100), dpi=100)
    plt.hist(scores, color='lightblue', edgecolor='black', bins=np.arange(max(scores)+2)-0.5, align="mid")
    plt.xticks(range(max(scores)))

    quant = int(100*(scores[:-1]<scores[-1]).mean())

    plt.axvline(x=scores[-1], color='red')
    plt.title(f'You scored {scores[-1]}.\nThis is better than {quant}% of all players.')
    plt.savefig('scores/sequence_memory.png')
