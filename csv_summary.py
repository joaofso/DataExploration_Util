#!/usr/bin/env python3

from argparse import ArgumentParser
import sys
import os
import pandas as pd
import numpy as np
from pandas.errors import ParserError


def get_command_parser():
    parser = ArgumentParser(description='Runs a simple textual summary on the provided csv file.')
    # positional arguments
    parser.add_argument('file', type=str, nargs='?', help='location of the CSV file')
    parser.add_argument('-c', '--columns', nargs='+', default=[], help='list of columns to be summarized')
    parser.add_argument('-l', '--list-columns', dest='list', action='store_true',
                        help='prints a list of columns available to be summarized')
    parser.add_argument('-sep', '--separator', dest='separator', default=';',
                        help='separator used as field delimiter of the CSV files (\';\' is the default separator)')
    return parser


def check_parameters():
    parameter_parser = get_command_parser()
    args = parameter_parser.parse_args()

    if not args.file and not sys.stdin.isatty():
        args.file = sys.stdin

    if not args.file:
        raise Exception('File not present. Provide an input file.')

    return args


def is_csv(file_path):
    return file_path.endswith('.csv')


def perform_summary(args):
    try:
        df = pd.read_csv(args.file, sep=args.separator, engine='python')
        columns = args.columns if args.columns else df.columns
        sub_df = df[columns]
        calculate_metrics(sub_df)
    except ParserError as exc:
        print('The provided separator {} is incompatible with the provided file or the provided file is not a valid CSV'
              .format(args.separator))


def calculate_metrics(df):
    summary = df.describe(include=[np.number])
    print(summary)
    perc_99 = df.quantile(q=0.99)
    print(f'99-quantile: {perc_99}')


if __name__ == '__main__':
    try:
        arguments = check_parameters()
        if arguments.list:
            dataframe = pd.read_csv(arguments.file, sep=arguments.separator, engine='python')
            print(dataframe.columns.tolist())
        else:
            perform_summary(arguments)
        sys.exit(0)
    except Exception as ex:
        print(ex)
        sys.exit(1)
