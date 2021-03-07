[![ci](https://github.com/zavolanlab/tin-score-calculation/workflows/ci/badge.svg?branch=dev)](https://github.com/zavolanlab/tin-score-calculation/actions?query=workflow%3Aci)
[![CodeFactor](https://www.codefactor.io/repository/github/zavolanlab/tin-score-calculation/badge)](https://www.codefactor.io/repository/github/zavolanlab/tin-score-calculation)
[![GitHub issues](https://img.shields.io/github/issues/zavolanlab/tin-score-calculation)](https://github.com/zavolanlab/tin-score-calculation/issues)
[![GitHub license](https://img.shields.io/github/license/zavolanlab/tin-score-calculation)](https://github.com/zavolanlab/tin-score-calculation/blob/dev/LICENSE)

# TIN score calculation

Given a set of BAM files and a gene annotation BED file, calculates the
Transcript Integrity Number (TIN) for each transcript.

## Main usage

```sh
python tin_score_calculation.py [-h] [options]
```

### Parameters

```console
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -i INPUT_FILES, --input=INPUT_FILES
                        Input BAM file(s). "-i" takes these input: 1) a single
                        BAM file. 2) "," separated BAM files (no spaces
                        allowed). 3) directory containing one or more bam
                        files. 4) plain text file containing the path of one
                        or more bam files (Each row is a BAM file path). All
                        BAM files should be sorted and indexed using samtools.
                        [required]
  -r REF_GENE_MODEL, --refgene=REF_GENE_MODEL
                        Reference gene model in BED format. Must be strandard
                        12-column BED file. [required]
  -c MINIMUM_COVERAGE, --minCov=MINIMUM_COVERAGE
                        Minimum number of read mapped to a transcript.
                        default=10
  -n SAMPLE_SIZE, --sample-size=SAMPLE_SIZE
                        Number of equal-spaced nucleotide positions picked
                        from mRNA. Note: if this number is larger than the
                        length of mRNA (L), it will be halved until it's
                        smaller than L. default=100
  --names=SAMPLE_NAMES  sample names, comma separated (no spaces allowed);
                        number must match the number of provided bam_files
  -s, --subtract-background
                        Subtract background noise (estimated from intronic
                        reads). Only use this option if there are substantial
                        intronic reads.
```

### File formats

- [BAM](https://samtools.github.io/hts-specs/SAMv1.pdf)
- [BED](https://www.ensembl.org/info/website/upload/bed.html)

Sample output ([TSV](https://en.wikipedia.org/wiki/Tab-separated_values)):

```console
transcript         sample_name
ENST00000303113    80.6328743265
ENST00000427445    0
ENST00000430792    59.7324017312
ENST00000647504    84.8860204563
ENST00000398647    64.4764470574
ENST00000400202    69.6331415873
ENST00000455813    85.3605191157
ENST00000397854    92.3965306733
ENST00000630077    72.8829044591
```

### Information

The tool was forked off the script `tin.py` (v2.6.4) of the
[`RSeQC`](http://rseqc.sourceforge.net/) package to achieve some speed-up.

This program calculates transcript integrity number (TIN) for each transcript
(or gene) in BED file. TIN is conceptually similar to RIN (RNA integrity number)
but provides transcript level measurement of RNA quality and is more sensitive
to measure low quality RNA samples:

1. TIN score of a transcript is used to measure the RNA integrity of the
transcript.
2. Median TIN score across all transcripts can be used to measure RNA integrity
of that "RNA sample".
3. TIN ranges from 0 (the worst) to 100 (the best). TIN = 60 means: 60% of the
transcript has been covered if the reads coverage were uniform.
4. TIN will be assigned to 0 if the transcript has no coverage or covered reads
is fewer than cutoff.

## Extended usage

Additionaly, this repository has been updated with two simple Python scripts:

### TIN score merge

Merge TIN score TSV tables for multiple input samples.

```sh
python tin_score_merge.py [-h] [options]
```

### Parameters

```console
  -h, --help            show this help message and exit
  -v {DEBUG,INFO,WARN,ERROR,CRITICAL}, --verbosity {DEBUG,INFO,WARN,ERROR,CRITICAL}
                        Verbosity/Log level. Defaults to ERROR
  -l LOGFILE, --logfile LOGFILE
                        Store log to this file.
  --input-files INFILES
                        Space-separated paths to the input tables.
  --output-file OUTFILE
                        Path for the outfile with merged TIN scores
```

Output file is formatted in a TSV table as well.

### TIN score plot

Create per-sample [boxplots](https://en.wikipedia.org/wiki/Box_plot) of TIN scores.

```sh
python tin_score_plot.py [-h] [options]
```

### Parameters

```console
  -h, --help            show this help message and exit
  -v {DEBUG,INFO,WARN,ERROR,CRITICAL}, --verbosity {DEBUG,INFO,WARN,ERROR,CRITICAL}
                        Verbosity/Log level. Defaults to ERROR
  -l LOGFILE, --logfile LOGFILE
                        Store log to this file.
  --input-file INFILE   Path to the table with merged TIN scores
  --output-file-prefix OUTFILE_PREFIX
                        Prefix for the path to the TIN boxplots.
```

The boxplots are generated in [PDF](https://en.wikipedia.org/wiki/PDF) and
[PNG](https://en.wikipedia.org/wiki/Portable_Network_Graphics) formats under
`output-file-prefix`+`.pdf` and `output-file-prefix`+`.png`.

## Run locally

In order to use the scripts, you will need to clone the repository and install
the dependencies:

```sh
git clone https://git.scicore.unibas.ch/zavolan_group/tools/tin_score_calculation
cd tin_score_calculation
pip install -r requirements.txt
# Optional: run tests
pytest
```

> **NOTES:**  
>  
> - You may want to install dependencies inside a virtual environment,
>   e.g., using [`virtualenv`](https://virtualenv.pypa.io/en/latest/).
> - Some of the dependencies require specific system libraries to be installed.

You can then find the scripts in directory `src/` and run it as described in
the [Main usage](#main-usage) and [Extended usage](#extended-usage) sections.
To run the tool with minimum test files, try:

```sh
python src/tin_score_calculation.py -i tests/test.bam -r tests/test.bed --names "sample_name"
python src/tin_score_merge.py --input-files test/test_TIN1.tsv,test/test_TIN2.tsv --output-file tests/TIN_merged.tsv
python src/tin_score_plot.py --input-file tests/test_TIN_merged.tsv --output-file-prefix tests/TIN_boxplots
```

## Run inside container

If you have [Docker](https://www.docker.com/) installed, you can also pull the
Docker image:

```sh
docker pull zavolab/tin_score_calculation:0.3.0
```

The scripts can be found in directory `/home/user/tin_score_calculation/src`
inside the Docker container. You can verify they are working by running, e.g.:

```sh
docker run --rm zavolab/tin_score_calculation:0.3.0 -i tests/test.bam -r tests/test.bed --names "sample_name"
```

> **NOTE:** To run the tool on your own data in that manner, you will probably
> need to [mount a volume](https://docs.docker.com/storage/volumes/) to allow
> the container read input files and write persistent output from/to the host
> file system.

## Tags

bioinformatics, quality control, rna-seq, bam, bed, tsv, transcript integrity

## Version

0.3.0

## Contact

- Maintainer: [Mihaela Zavolan](https://git.scicore.unibas.ch/zavolan)
- Affiliation: Zavolan lab, Biozentrum, University of Basel
- Email: mihaela.zavolan@unibas.ch
