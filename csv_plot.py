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
    parser.add_argument('file', type=str, nargs='?', help='location of the CSV file')

    parser.add_argument('-x', '--x-axis', nargs='*', dest='x', default=[],
                        help='list of columns to be considered as x-axis for scatter plots and samples for the boxplots')

    parser.add_argument('-y', '--y-axis', nargs='*', dest='y', default=[],
                        help='list of columns to be considered as y-axis for scatter plots')

    parser.add_argument('-sep', '--separator', dest='separator', default=';',
                        help='separator used as field delimiter of the CSV files (\';\' is the default separator)')

    parser.add_argument('-l', '--list-columns', dest='list', action='store_true',
                        help='prints a list of columns available to be plotted')

    parser.add_argument('-f', '--save_file', dest='out', help='saves the graphs in a file')

    parser.add_argument('-g', '--graph', dest='graph', choices=['scatter', 'box'], default='scatter')
    return parser


def check_parameters(parameters):
    parameter_parser = get_command_parser()
    args = parameter_parser.parse_args(parameters)

    if not args.file and not sys.stdin.isatty():
        args.file = sys.stdin

    if not args.file:
        raise Exception('File not present. Provide an input file.')

    if not args.list:
        if args.graph is 'scatter' and not args.y:
            raise Exception('Provide a list of column to be considered as y-axis')

    if args.out and not args.out.endswith('.png'):
        args.out = args.out + '.png'
    return args


def clean_dataframe_header(df: pandas.DataFrame):
    df.columns = list(map(str.strip, df.columns))


def plot_scatter(args):
    try:
        dataframe = pandas.read_csv(args.file, sep=args.separator, engine='python')
        clean_dataframe_header(dataframe)

        for field in set(args.x + args.y):
            if field not in dataframe.columns:
                raise Exception('The column {} is not present in the provided csv file'.format(field))

        if not args.x:
            args.x = ['fake_column']
            r = range(0, len(dataframe.iloc[:, 0]))
            dataframe['fake_column'] = r

        figure, graphs = plot.subplots(nrows=len(args.y), ncols=len(args.x), squeeze=False, sharex='col', sharey='row')

        for index_x, x in enumerate(args.x):
            for index_y, y in enumerate(args.y):
                x_sample = dataframe[x]
                y_sample = dataframe[y]
                graphs[index_y, index_x].scatter(x=x_sample, y=y_sample)
                graphs[index_y, index_x].set_xlabel(x if x is not 'fake_column' else '')
                for tick_marks in graphs[index_y, index_x].get_xticklabels():
                    tick_marks.set_rotation(45)
                graphs[index_y, index_x].set_ylabel(y)
        plot.show()
    except ParserError as exc:
        print('The provided separator {} is incompatible with the provided file'.format(args.separator))


def plot_boxplot(args):
    try:
        dataframe = pandas.read_csv(args.file, sep=args.separator)
        for field in args.x:
            if field not in dataframe.columns:
                raise Exception('The column {} is not present in the provided csv file'.format(field))

        figure, graphs = plot.subplots(ncols=len(args.x))

        for index_x, x in enumerate(args.x):
            x_sample = dataframe[x]
            graphs[index_x].boxplot(x_sample)
            graphs[index_x].set_xlabel(x)
        plot.show()
    except ParserError as exc:
        print('The provided separator {} is incompatible with the provided file'.format(args.separator))


def generate_plots(args):
    if args.graph == 'scatter':
        plot_scatter(args)
    elif args.graph == 'box':
        plot_boxplot(args)


if __name__ == '__main__':
    try:
        arguments = check_parameters(sys.argv[1:])
        if arguments.list:
            dataframe = pandas.read_csv(arguments.file, sep=arguments.separator, engine='python')
            print(dataframe.columns.tolist())
        else:
            generate_plots(arguments)
        sys.exit(0)
    except Exception as ex:
        print(ex)
        sys.exit(1)
