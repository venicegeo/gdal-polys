import argparse
import os
import subprocess
import random
import datetime
import re
import multiprocessing as mp
import beachtools as bt


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--small_lines",
                        default=None,
                        type=str,
                        help="name of smaller geojson containing linestrings of coastline")
    parser.add_argument("--large_lines",
                        default="None",
                        type=str,
                        help="name of larger geojson containing linestrings of coastline")

    parser.add_argument("--out_name",
                        default='beachfront_poly.shp',
                        type=str,
                        help="name of output shape file")
    return(parser)


def main():
    args = create_parser().parse_args()
    smalls, larges = bt.read_gjsons(args.small_lines, args.large_lines)
    merged = bt.trim_and_merge(smalls, larges)
    final_ta = bt.make_and_write_ta(merged, args.out_name)
    bt.print_report(final_ta, args.out_name)


if __name__ == "__main__":
    main()
