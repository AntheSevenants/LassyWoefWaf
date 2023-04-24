# Prepare for a wild ride

import time
import argparse
import re
import concurrent.futures
import pandas as pd

from pathlib import Path
from tqdm.auto import tqdm
from woef.Common import get_country_from_cmdi_file, get_country_from_cmdi_file_lxml
from woef.Countries import Countries

#
# Argument parsing
#

parser = argparse.ArgumentParser(
    description='LassyWoefWaf - generate easy meta information for SoNaR')
parser.add_argument('sonar_500_cmdi_path', type=str,
                    help='Path to the SONAR500 CMDI directory')
parser.add_argument('sonar_new_media_cmdi_path', type=str,
                    help='Path to the SONAR500 CMDI directory')
parser.add_argument('--output_path', type=str, nargs='?',
                    default='SonarMeta.csv', help='Name of the output file')

args = parser.parse_args()

# Start the performance counter
t1 = time.perf_counter()

cmdi_files = set(Path(args.sonar_500_cmdi_path).rglob("*.cmdi.xml"))
cmdi_new_media_files = set(Path(
    args.sonar_new_media_cmdi_path).rglob("*.cmdi.xml"))

# We load all CMDI files. These contain the metadata we're interested in.
# There are too many to keep them in memory, so I just keep their length for progress purposes
cmdi_length = len(cmdi_files)
cmdi_new_media_length = len(cmdi_new_media_files)

print("Found", cmdi_length + cmdi_new_media_length, "CMDI files")

document_ids = []
countries = []

def get_cmdi_meta(pfin):
    cmdi_path = str(pfin)
    document_id = pfin.stem.replace(".cmdi", "")
    country = get_country_from_cmdi_file(cmdi_path)

    return (document_id, country)


def cmdi_process(iterator, total, desc):
    # Don't shoot me OK
    global document_ids
    global countries

    for cmdi_file in tqdm(iterator, total=total, desc=desc):
        document_id, country = get_cmdi_meta(cmdi_file)

        # Add the found results to the current results
        document_ids.append(document_id)
        countries.append(country)

cmdi_process(cmdi_files, cmdi_length, "CMDI files")
cmdi_process(cmdi_new_media_files,
             cmdi_new_media_length, "CMDI New Media files")

# Create a data frame from the results
df = pd.DataFrame({"document": document_ids,
                   "country": countries})
df = df.sort_values("document")
df = df.drop_duplicates(subset="document", keep="last")

df.to_csv(args.output_path, index=None)

t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')
