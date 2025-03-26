from setuptools import setup, find_packages

setup(
    name="data_exploration",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # list your dependencies here
        'pandas',
        'numpy',
        'argparse',
    ],
    scripts=[
        'data_exploration/scripts/csv_summary.py',
        'data_exploration/scripts/csv_plot.py',
    ],
)