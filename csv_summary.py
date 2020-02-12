#!/usr/bin/python2

from argparse import ArgumentParser
import sys
import os
import pandas as pd
import numpy as np
from pandas.errors import ParserError


def get_command_parser():
    parser = ArgumentParser(description='Runs a simple textual summary on the provided csv file.')
    # positional arguments
    parser.add_argument('file', help='location of the CSV file')
    parser.add_argument('-c', '--columns', nargs='+', default=[], help='list of columns to be summarized')
    parser.add_argument('-sep', '--separator', dest='separator', default=';',
                        help='separator used as field delimiter of the CSV files (\';\' is the default separator)')
    return parser


def check_parameters():
    parameter_parser = get_command_parser()
    args = parameter_parser.parse_args()
    if not args.file:
        raise Exception('File not present. Provide an input file.')

    if not os.path.exists(args.file):
        raise Exception('The provided file does not exist.')

    if not is_csv(args.file):
        raise Exception('The provided file is not a csv.')

    return args


def is_csv(file_path):
    return file_path.endswith('.csv')


def perform_summary(args):
    try:
        dataframe = pd.read_csv(args.file, sep=args.separator)
        columns = args.columns if args.columns else dataframe.columns
        sub_dataframe = dataframe[columns]
        calculate_metrics(sub_dataframe)
    except ParserError as exc:
        print('The provided separator {} is incompatible with the provided file'.format(args.separator))

def calculate_metrics(df):
    summary = df.describe(include=[np.number])
    print(summary)


if __name__ == '__main__':
    try:
        arguments = check_parameters()
        perform_summary(arguments)
        sys.exit(0)
    except Exception as ex:
        print(ex)
        sys.exit(1)
