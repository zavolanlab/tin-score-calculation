#!/usr/bin/env python
##############################################################################
#
#   Generate simple statistics for the per-sample TIN scores.
#
#   AUTHOR: Maciej_Bak
#   AFFILIATION: University_of_Basel
#   CONTACT: wsciekly.maciek@gmail.com
#   CREATED: 12-08-2021
#
##############################################################################

# imports
import time
import logging
import logging.handlers
from argparse import ArgumentParser, RawTextHelpFormatter
import numpy as np
import pandas as pd


def parse_arguments():
    """Parser of the command-line arguments."""
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument(
        "-v",
        "--verbosity",
        dest="verbosity",
        choices=("DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"),
        default="ERROR",
        help="Verbosity/Log level. Defaults to ERROR",
    )
    parser.add_argument(
        "-l", "--logfile", dest="logfile", help="Store log to this file."
    )
    parser.add_argument(
        "--input-file",
        dest="infile",
        required=True,
        help="Path to the table with merged TIN scores",
    )
    parser.add_argument(
        "--output-file",
        dest="outfile",
        required=True,
        help="Path for the output table with TIN statistics.",
    )
    return parser


##############################################################################


def main():
    """Main body of the script."""

    merged = pd.read_csv(options.infile, sep="\t", index_col=0)
    summary = pd.DataFrame(columns=merged.columns)
    summary.loc["min.TIN"] = [round(np.min(merged[c].dropna()), 2) for c in merged.columns]
    summary.loc["Q1.TIN"] = [round(np.percentile(merged[c].dropna(), 25), 2) for c in merged.columns]
    summary.loc["Median.TIN"] = [round(np.median(merged[c].dropna()), 2) for c in merged.columns]
    summary.loc["Q3.TIN"] = [round(np.percentile(merged[c].dropna(), 75), 2) for c in merged.columns]
    summary.loc["max.TIN"] = [round(np.max(merged[c].dropna()), 2) for c in merged.columns]
    summary.loc["Avg.TIN"] = [round(np.mean(merged[c].dropna()), 2) for c in merged.columns]
    summary.loc["St.dev.TIN"] = [round(np.std(merged[c].dropna()), 2) for c in merged.columns]
    summary.to_csv(options.outfile, sep="\t")


##############################################################################


if __name__ == "__main__":

    try:
        # parse the command-line arguments
        options = parse_arguments().parse_args()

        # set up logging during the execution
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s\
                                      - %(message)s",
            datefmt="%d-%b-%Y %H:%M:%S",
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger = logging.getLogger("uniprot_to_json")
        logger.setLevel(logging.getLevelName(options.verbosity))
        logger.addHandler(console_handler)
        if options.logfile is not None:
            logfile_handler = logging.handlers.RotatingFileHandler(
                options.logfile, maxBytes=50000, backupCount=2
            )
            logfile_handler.setFormatter(formatter)
            logger.addHandler(logfile_handler)

        # execute the body of the script
        start_time = time.time()
        logger.info("Starting script")
        main()
        seconds = time.time() - start_time

        # log the execution time
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        logger.info(
            "Successfully finished in {hours} hour(s) \
{minutes} minute(s) and {seconds} second(s)",
            hours=int(hours),
            minutes=int(minutes),
            seconds=int(seconds) if seconds > 1.0 else 1,
        )
    # log the exception in case it happens
    except Exception as e:
        logger.exception(str(e))
        raise e
