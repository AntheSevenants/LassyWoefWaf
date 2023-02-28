import time
import argparse
import os
import pandas as pd

from pathlib import Path
from lxml import etree

from Countries import Countries

#
# Argument parsing
#

parser = argparse.ArgumentParser(description='LassyWoefWaf - generate meta information for Lassy Klein')
parser.add_argument('lassy_klein_path', type=str,
					help='Path to the LassyKlein')
parser.add_argument('--output_path', type=str, nargs='?', default='LassyKleinMeta.csv', help='Name of the output file')

args = parser.parse_args()

# Start the performance counter
t1 = time.perf_counter()

alpino_corpus_path = f"{args.lassy_klein_path}/Treebank/"
sonar_cmdi_path = f"{args.lassy_klein_path}/META/sonar500/"

# I remove the first item because it's just the parent directory (= "Treebank")
documents = [Path(x[0]).stem for x in os.walk(alpino_corpus_path)][1:]
cmdi_files = list(Path(sonar_cmdi_path).rglob("*.cmdi.xml"))
cmdi_files_stems = [Path(x).stem.replace(".cmdi", "") for x in cmdi_files]

print("Found", len(documents), "documents")
print("Found", len(cmdi_files), "CMDI files")

def process_document(directory_name):
    country = "UNK"

    # Infer from the ~vannoord file
    # http://www.let.rug.nl/~vannoord/Lassy/Lassy-Klein-Groot.txt

    prefix = directory_name[0:7]
    if prefix in [ "dpc-bal", "dpc-bmm", "dpc-kok", "dpc-svb" ]:
        country = Countries.NETHERLANDS
    elif prefix in [ "dpc-cam", "dpc-dns", "dpc-fsz", "dpc-gaz", "dpc-med",
                     "dpc-qty", "dpc-riz", "dpc-rou", "dpc-vhs", "dpc-vla",
                     "dpc-kam" ]:
        country = Countries.BELGIUM
    elif prefix in [ "dpc-eli", "dpc-eup", "dpc-ibm" ]:
        pass

    # Not found? Refer to the CMDI files included in the CCL LassyKlein version
    if directory_name in cmdi_files_stems:
        cmdi_file_index = cmdi_files_stems.index(directory_name)

        root = etree.parse(cmdi_files[cmdi_file_index])
        # I HATE NAMESPACES
        country_nodes = root.xpath("//*[local-name() = 'Source']/*[local-name() = 'Country']")

        if len(country_nodes) > 0:
            element_text = country_nodes[0].text
            if element_text == "NL":
                country = Countries.NETHERLANDS
            elif element_text == "B":
                country = Countries.BELGIUM

    # Still not found? God only knows...

    return country

country_info = [process_document(document) for document in documents]

df = pd.DataFrame({"document": documents,
                   "country": country_info})

df.to_csv(args.output_path, index=None)

t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')