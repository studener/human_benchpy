import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def make_plot(game: str):
    df = pd.read_csv(f'scores/{game}.csv')
    scores = np.array(df.Scores)

    plt.figure(figsize=(720/100, 500/100), dpi=100)
    plt.xlabel("Score")
    
    if game == "aim_trainer" or game == "verbal_memory":
        if game == "aim_trainer":
            plt.xlabel("Time in Milliseconds")
        bins = 20 #np.arange(min(scores)-2, max(scores)+2)-0.5
    else:
        plt.xticks(range(max(scores)+1))
        bins = np.arange(max(scores)+2)-0.5

    plt.hist(scores, color='lightblue', edgecolor='black', bins=bins, align="mid")

    if len(scores) == 1:
        quant = 100
    else:
        quant = int(100*(scores[:-1]<scores[-1]).mean())

    plt.axvline(x=scores[-1], color='red')
    if game == "aim_trainer":
        plt.title(f'You took {scores[-1]}ms on average.\nThis is faster than {100-quant}% of all players.')
    else:
        plt.title(f'You scored {scores[-1]}.\nThis is better than {quant}% of all players.')
    plt.savefig(f'scores/{game}.png')
