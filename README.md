# LassyWoefWaf
What's in the Lassy corpora? You tell me!

I was surprised to learn that the [Lassy Klein](https://taalmaterialen.ivdnt.org/download/lassy-klein-corpus6/) and [Lassy Groot](https://taalmaterialen.ivdnt.org/download/tstc-lassy-groot-corpus/) corpora do not ship with information on what region the materials in the corpus come from. This region information is *out there* (mostly), but one has to collect bits and pieces from different locations. With the scripts in this repository, I aim to assign a region (either 'Belgium', 'The Netherlands' or 'Unknown') to each document in each of the two corpora.

If you are not interested in reproducing my results, you can download the extracted region information from the [Releases](https://github.com/AntheSevenants/LassyWoefWaf/releases).

## My sources

* Gertjan van Noord has put together an [overview](http://www.let.rug.nl/~vannoord/Lassy/Lassy-Klein-Groot.txt) of the contents of Lassy Klein and Lassy Groot. From this overview, region information can be inferred (but not for every section).
* The Lassy corpora share a lot of documents with [SONAR](https://taalmaterialen.ivdnt.org/download/tstc-sonar-corpus/). SONAR *does* ship with meta information on its documents, so we can use the information from SONAR for Lassy.

## Prerequisites

### Corpora

To extract Lassy Klein region information, you only need Lassy Klein:

* [Lassy Klein](https://taalmaterialen.ivdnt.org/download/lassy-klein-corpus6/)  
    Warning: the version offered by the IVDNT does not contain the meta files! I do not know why!

To extract Lassy Groot region information, you need Lassy Groot and SONAR:

* [Lassy Groot](https://taalmaterialen.ivdnt.org/download/tstc-lassy-groot-corpus/)
* [SONAR](https://taalmaterialen.ivdnt.org/download/tstc-sonar-corpus/)

### Preparation

These instructions only have to be run once.

1. Download and install [Python](https://www.python.org/).
2. `git clone https://github.com/AntheSevenants/LassyWoefWaf.git`,   
    or download and unzip [this archive](https://github.com/AntheSevenants/LassyWoefWaf/archive/refs/heads/main.zip).
3. Open a terminal window. Navigate to the `LassyWoefWaf` directory:  
    `cd LassyWoefWaf`
4. Create a new virtual environment:  
    `python -m venv venv` or `python3 -m venv venv`
5. Activate the virtual environment:  
    `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (unix)
6. Install all dependencies:  
    `pip install -r requirements.txt`

### Running

These instructions need to be followed every time you want to use the LassyWoefWaf program.

1. Open a terminal window. Navigate to the `LassyWoefWaf` directory:  
    `cd LassyWoefWaf`
2. Activate the virtual environment:  
    `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (unix)
3. You can now run any of the scripts detailed below.

## Extracting region information

### Lassy Klein

To extract the region information for Lassy Klein, I used a combination of Gertjan van Noord's overview and the CMDI files included in the copy of Lassy Klein that was given to me by the [CCL](https://www.arts.kuleuven.be/ling/ccl). If you download Lassy Klein from the link above, these CMDI files are not included. Maybe they come from somewhere else, but I do not have the time to track down their origin. Unfortunately, this means that for Lassy Klein, my region extraction process becomes less reproducible (unless you also get a copy of Lassy Klein from the CCL).

In any case, this is the command you should run to infer Lassy Klein region information (given that you have the CCL version):

```bash
python3 LassyKlein.py "/path/to/lassy klein/"
```

### Lassy Groot

To extract the region information for Lassy Groot, I used the CMDI files included in SONAR. You do not need any special internal CCL versions of these corpora, so this process is maximally reproducible (given that you have the patience to download and extract these corpora).

This is the command you should run to infer Lassy Groot region information:

```bash
python3 LassyGroot.py "/path_to_lassy_groot/data/" "/path_to_sonar/SONAR500/CMDI/"
```

The script will use all your cores to compute the region information as fast as possible.