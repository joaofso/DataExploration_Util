#!/usr/bin/env python3

from argparse import ArgumentParser
import sys
import os
import pandas
import matplotlib.pyplot as plot
from pandas.errors import ParserError


def get_command_parser():
    parser = ArgumentParser(description='Plots the desired graphs based on the information from the provided csv file.')
    # positional arguments
    parser.add_argument('file', help='location of the CSV file')

    parser.add_argument('-x', '--x-axis', nargs='*', dest='x', default=[],
                        help='list of columns to be considered as x-axis')

    parser.add_argument('-y', '--y-axis', nargs='*', dest='y', default=[],
                        help='list of columns to be considered as y-axis')

    parser.add_argument('-sep', '--separator', dest='separator', default=';',
                        help='separator used as field delimiter of the CSV files (\';\' is the default separator)')

    parser.add_argument('-l', '--list-columns', dest='list', action='store_true',
                        help='prints a list of columns available to be plotted')

    parser.add_argument('-f', '--save_file', dest='out', help='saves the graphs in a file')
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

    if not args.list:
        if not args.x:
            raise Exception('Provide a list of column to be considered as x-axis')
        if args.y:
            raise Exception('Provide a list of column to be considered as y-axis')

    if args.out and not args.out.endswith('.png'):
        args.out = args.out + '.png'
    return args


def is_csv(file_path):
    return file_path.endswith('.csv')


def generate_plots(args):
    try:
        dataframe = pandas.read_csv(args.file, sep=args.separator)
        for field in set(args.x, args.y):
            if field not in dataframe.columns:
                raise Exception('The column {} is not present in the provided csv file'.format(field))

        number_graphs = len(args.x) * len(args.y)
        current_graph = 0
        figure, graphs = plot.subplots(nrows=number_graphs)

        for x in args.x:
            for y in args.y:
                x_sample = dataframe[x]
                y_sample = dataframe[y]
                graphs[current_graph].scatter(x=x_sample, y=y_sample)
                graphs[current_graph].xlabel(x)
                graphs[current_graph].ylabel(y)
                current_graph += 1

        plot.show()

    except ParserError as exc:
        print('The provided separator {} is incompatible with the provided file'.format(args.separator))

if __name__ == '__main__':
    try:
        arguments = check_parameters()
        if arguments.list:
            dataframe = pandas.read_csv(arguments.file, sep=arguments.separator)
            print(dataframe.columns.tolist())
        else:
            generate_plots(arguments)
        sys.exit(0)
    except Exception as ex:
        print(ex)
        sys.exit(1)
