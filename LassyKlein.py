import time
import argparse
import os
import pandas as pd

from pathlib import Path
from Countries import Countries

#
# Argument parsing
#

parser = argparse.ArgumentParser(description='LassyWoefWaf - generate meta information for Lassy Klein')
parser.add_argument('alpino_corpus_path', type=str,
					help='Path to the Alpino corpus files for LassyKlein')
parser.add_argument('--output_path', type=str, nargs='?', default='LassyKleinMeta.csv', help='Name of the output file')

args = parser.parse_args()

# Start the performance counter
t1 = time.perf_counter()

documents = [Path(x[0]).stem for x in os.walk(args.alpino_corpus_path)]

def process_document(directory_name):
    country = "UNK"

    prefix = directory_name[0:7]

    if prefix in [ "dpc-bal", "dpc-bmm", "dpc-kok", "dpc-svb" ]:
        country = Countries.NETHERLANDS
    elif prefix in [ "dpc-cam", "dpc-dns", "dpc-fsz", "dpc-gaz", "dpc-med",
                     "dpc-qty", "dpc-riz", "dpc-rou", "dpc-vhs", "dpc-vla",
                     "dpc-kam" ]:
        country = Countries.BELGIUM
    elif prefix in [ "dpc-eli", "dpc-eup", "dpc-ibm" ]:
        pass

    return country

country_info = [process_document(document) for document in documents]

df = pd.DataFrame({"document": documents,
                   "country": country_info})

df.to_csv(args.output_path, index=None)

t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')