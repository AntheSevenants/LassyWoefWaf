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
fig = ax.get_figure()
fig.savefig("out.png") 