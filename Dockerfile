##### BASE IMAGE #####
FROM python:2.7.17-slim-stretch as build

##### METADATA #####
LABEL base.image="python:2.7.17-slim-stretch"
LABEL software="tin_score_calculation"
LABEL software.version="0.3.0"
LABEL software.description="Given a set of BAM files and a gene annotation BED file, calculates the Transcript Integrity Number (TIN) for each transcript"
LABEL software.website="https://git.scicore.unibas.ch/zavolan_group/tools/tin_score_calculation"
LABEL software.documentation="https://git.scicore.unibas.ch/zavolan_group/tools/tin_score_calculation/blob/master/README.md"
LABEL software.license="https://git.scicore.unibas.ch/zavolan_group/tools/tin_score_calculation/blob/master/LICENSE"
LABEL software.tags="bioinformatics, quality control, rna-seq, bam, bed, tsv, transcript integrity"
LABEL maintainer="Mihaela Zavolan"
LABEL maintainer.email="mihaela.zavolan@unibas.ch"
LABEL maintainer.organisation="Zavolan lab, Biozentrum, University of Basel"

##### VARIABLES #####
ENV PACKAGES libbz2-dev liblzma-dev zlib1g-dev gcc+ make

##### INSTALLATION #####
RUN apt-get update -y \
  && apt-get install -y --no-install-recommends ${PACKAGES} \
  && rm -rf /var/lib/apt/lists/*
COPY ./requirements.txt /requirements/requirements.txt
RUN pip install -r /requirements/requirements.txt
COPY src/tin_score_calculation.py /usr/bin/
COPY src/tin_score_merge.py /usr/bin/
COPY src/tin_score_plot.py /usr/bin/

#### CLEAN IMAGE ####
FROM python:2.7.17-slim-stretch
COPY --from=build /usr/bin/tin_score_calculation.py /usr/bin/
COPY --from=build /usr/bin/tin_score_merge.py /usr/bin/
COPY --from=build /usr/bin/tin_score_plot.py /usr/bin/
COPY --from=build /usr/local/lib/python2.7/site-packages/ /usr/local/lib/python2.7/site-packages/

