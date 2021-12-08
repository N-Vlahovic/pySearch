#!/usr/bin/env python3
import argparse
from typing import NoReturn

from .pySearch import search, PYPI_MAX_RES_PER_PAGE


parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument(
    "query",
    help="Search query",
    type=str,
)
parser.add_argument(
    "-l",
    "--limit",
    help="The maximal number of results to display",
    required=False,
    default=PYPI_MAX_RES_PER_PAGE,
    type=int,
)
args: argparse.Namespace = parser.parse_args()


def main() -> NoReturn:
    search(q=args.query)
