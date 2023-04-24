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
    description='LassyWoefWaf - generate meta information for Lassy Groot, using... SONAR?')
parser.add_argument('lassy_groot_data_path', type=str,
                    help='Path to the LassyGroot data directory')
parser.add_argument('sonar_500_cmdi_path', type=str,
                    help='Path to the SONAR500 CMDI directory')
parser.add_argument('--output_path', type=str, nargs='?',
                    default='LassyGrootMeta.csv', help='Name of the output file')

args = parser.parse_args()

# Start the performance counter
t1 = time.perf_counter()

# First, we want to get all the .data files that LassyGroot contains
# These are joined XML files of individual sentences, but they're not valid XML combined
# (this is a story for another time)
data_files = list(Path(args.lassy_groot_data_path).rglob("*.data"))

print("Found", len(data_files), "data files")

# Then, there's the CMDI files. These contain the metadata we're interested in.
# I want to link the document names to their full paths, which is what I'm doing here
cmdi_files = set(Path(args.sonar_500_cmdi_path).rglob("*.cmdi.xml"))
cmdi_files_stems = set([Path(x).stem.replace(".cmdi", "") for x in cmdi_files])
# Keys = stems, values = full paths
stems2files = dict(zip(cmdi_files_stems, cmdi_files))

# Dunno, maybe it helps with memory
del cmdi_files

print("Found", len(cmdi_files_stems), "CMDI files")

# Surprise! There's no need to actually parse the XML files.
# The structure is always exactly the same, so pardon my regular expression heresy
id_re = re.compile("\"(.*?)\..*?\"")


def filter_file(pfin):
    # There are multiple sentences from the same document in these data files
    # So, I keep a document cache (as a set, because of performance reasons)
    # This way we can check whether we can skip a sentence because we already know its document
    doc_cache = set()

    doc_ids_inner = []  # Collected document IDs
    countries_inner = []  # Collected countries

    # Open the data file
    with pfin.open("rt") as reader:
        # Go over each line (this is still faster than XML parsing)
        for line in reader:
            # Look for a sentence element (the spacing is always the same)
            if line.startswith("  <sentence"):
                # By default, declare the country unknown
                country = Countries.UNKNOWN

                # Look for the sentence ID in this sentence
                # And extract the document ID from it
                if match := id_re.search(line):
                    doc_id = match.group(1)

                    # If we've already processed this document, skip
                    if doc_id in doc_cache:
                        continue
                else:
                    # Sentence has no valid SoNaR sentence ID...
                    # Tough luck!
                    continue

                # Now, let's cross-reference with the CMDI files
                if doc_id in cmdi_files_stems:
                    # Get the full path from the document ID
                    cmdi_path = stems2files[doc_id]
                    # Then, let the CMDI processor handle the rest
                    country = get_country_from_cmdi_file(cmdi_path)
                else:
                    # If, for some reason, the document ID has no associated CMDI file,
                    # there's nothing we can do...
                    pass

                # Save the doc id and associated country
                doc_ids_inner.append(doc_id)
                countries_inner.append(country)

                doc_cache.add(doc_id)

    return doc_ids_inner, countries_inner


# Register a tqdm progress bar
progress_bar = tqdm(total=len(data_files), desc='Progress')

doc_ids = []
countries = []

# Start a processing pool
with concurrent.futures.ProcessPoolExecutor() as executor:
    # For each file, spawn a new process
    futures = [executor.submit(filter_file, file) for file in data_files]
    # Loop over future results as they become available
    for future in concurrent.futures.as_completed(futures):
        progress_bar.update(n=1)  # Increments counter
        # Unpack the tuple
        doc_ids_to_add, countries_to_add = future.result()

        # Add the found results to the current results
        doc_ids = doc_ids + doc_ids_to_add
        countries = countries + countries_to_add

# Create a data frame from the results
df = pd.DataFrame({"document": doc_ids,
                   "country": countries})
df = df.sort_values("document")
df = df.drop_duplicates(subset="document", keep="last")

df.to_csv(args.output_path, index=None)

t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')
