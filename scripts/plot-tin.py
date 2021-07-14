#!/usr/bin/env python
##############################################################################
#
#   Generate PDF and PNG boxplots of the per-sample TIN scores.
#
#   AUTHOR: Maciej_Bak
#   AFFILIATION: University_of_Basel
#   CONTACT: wsciekly.maciek@gmail.com
#   CREATED: 09-03-2020
#
##############################################################################

# imports
import time
import logging
import logging.handlers
from argparse import ArgumentParser, RawTextHelpFormatter
import pandas as pd
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402


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
        "--output-file-prefix",
        dest="outfile_prefix",
        required=True,
        help="Prefix for the path to the TIN boxplots.",
    )
    return parser


##############################################################################


def main():
    """Main body of the script."""

    merged = pd.read_csv(options.infile, sep="\t", index_col=0)

    plt.figure(figsize=(7, 4))

    if merged.shape[0] > 0:

        ax = plt.gca()
        ax = merged.plot(
            kind="box",
            ax=ax,
            color=dict(boxes="k", whiskers="k", medians="k", caps="k"),
            boxprops=dict(linestyle="-", linewidth=1.5),
            flierprops=dict(linestyle="-", linewidth=1.5),
            medianprops=dict(linestyle="-", linewidth=1.5),
            whiskerprops=dict(linestyle="-", linewidth=1.5),
            capprops=dict(linestyle="-", linewidth=1.5),
            showfliers=False,
            grid=True,
            rot=0,
        )

        plt.ylim([0, 100])
        plt.yticks([10 * i for i in range(0, 11)])
        ax.xaxis.grid(False)
        ax.yaxis.grid(color="black", linestyle="-", linewidth=0.5, alpha=0.5)

    plt.savefig(options.outfile_prefix + ".png", format="png")
    plt.savefig(options.outfile_prefix + ".pdf", format="pdf")


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
