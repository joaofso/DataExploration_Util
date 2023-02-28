#!/usr/bin/env python3

import pandas as pd
import scipy.stats as st
from numpy.random import normal


class SampleComparator:
    
    def __init__(self, significance):
        self._significance = significance

    def _run_mann_whitney(self, old_sample: pd.core.series.Series,  new_sample: pd.core.series.Series, alt_hypothesis):
        statistic, p_value = st.mannwhitneyu(old_sample, new_sample, alternative=alt_hypothesis)
        print(f"The p-value was {p_value}")
        return p_value < self._significance

    def are_samples_different(self, old_sample: pd.core.series.Series,  new_sample: pd.core.series.Series):
        return self._run_mann_whitney(old_sample, new_sample, alt_hypothesis='two-sided')

    def is_old_sample_greater(self, old_sample: pd.core.series.Series,  new_sample: pd.core.series.Series):
        return self._run_mann_whitney(old_sample, new_sample, alt_hypothesis='greater')

    def is_old_sample_lesser(self, old_sample: pd.core.series.Series,  new_sample: pd.core.series.Series):
        return self._run_mann_whitney(old_sample, new_sample, alt_hypothesis='less')


if __name__ == '__main__':

    old_dataframe = pd.read_csv("/home/eourjoa/vmr-cil-0005_ep01.csv")
    new_dataframe = pd.read_csv("/home/eourjoa/vmr-cil-0005_ep05.csv")

    old_cpu_sample_idle = old_dataframe["%nice"]
    new_cpu_sample_idle = new_dataframe["%nice"]


    comparator = SampleComparator(significance=0.05)
    print(comparator.are_samples_different(old_sample=old_cpu_sample_idle, new_sample=new_cpu_sample_idle))

