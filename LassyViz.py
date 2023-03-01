import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='LassyWoefWaf Viz - visualise distribution of documents')
parser.add_argument('csv_input', type=str,
					help='Path to the distribution CSV')

args = parser.parse_args()

df = pd.read_csv(args.csv_input)

sns.set(style="darkgrid")
ax = sns.countplot(x="country", data=df)

for i, bar in enumerate(ax.patches):
    h = bar.get_height()
    ax.text(
        i, # bar index (x coordinate of text)
        h+25, # y coordinate of text
        '{}'.format(int(h)),  # y label
        ha='center', 
        va='center', 
        fontweight='bold', 
        size=14)

fig = ax.get_figure()
fig.savefig(f"{args.csv_input}.png") 