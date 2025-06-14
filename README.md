## human_benchpy
This repo contains python clones of the brain games and cognitive tests found on [Human Benchmark](https://humanbenchmark.com). This is purely for fun and learning purposes.

### Currently Available Games:
- **Aim Trainer**: Click 15 targets as fast as possible.
- **Number Memory**: Try to remember number sequences of increasing length each round.
- **Sequence Memory**: Memorize a sequence of lit up squares, that gets longer each round.
- **Verbal Memory**: Remember if a word shown on screen has already been displayed.
- **Visual Memory**: Memorize the positions of multiple lit up squares at once.

### Installation / Utilization:
First clone the repository to your local machine, then install the dependencies by running
```bash
pip install -r requirements.txt
```

After that, you can play your desired game by running e.g.
```bash
python sequence_memory.py
```

After playing a game you will be able to see your score compared to other (dummy) scores. To remove the dummy data, you have to delete it manually from the .csv files in `/scores`.

Python 3.11 was used for the project.