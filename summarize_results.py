#!/usr/bin/env python

import csv
import logging
import os
import pandas as pd
from typing import List, Dict, Tuple

class MetricSummaryConfig:
    def __init__(self, metric: str, filter: Dict[str, list] = {}, groupby: List[List[str]] = [[]], summary_columns: List[str] = ["value"]) -> None:
        self.metric = metric
        self.filter = filter
        self.groupby = groupby
        self.summary_columns = summary_columns

class Summarizer:
    def __init__(self, summary_configs: List[MetricSummaryConfig] = []) -> None:
        self.summary_configs = summary_configs

    def summarize(self, raw_files_path: str, output_path: str = "./summary.dat"):
        for root_dir, dirs, files in os.walk(raw_files_path):
            for file in files:
                file_path = os.path.join(root_dir, file)
                if self._is_valid_csv(file_path):
                        print(file_path)
                        summaries = self._summarize_file(file_path, self._get_config(file))
                        for summmary in summaries:
                            print(summmary)
                        print("\n")
                else:
                    logging.warning(f"The file {file_path} is not a valid csv. Skipping it.")

    def _is_valid_csv(self, file_path: str):
        for dialect in csv.list_dialects():
            try: 
                with open(file_path, newline="") as csvfile:
                    reader = csv.reader(csvfile, dialect)
                    return True
            except csv.Error:
                continue
        return False

    def _get_config(self, metric_file):
        for config in self.summary_configs:
            if config.metric in metric_file:
                return config
        return MetricSummaryConfig(metric_file)

    def _cleanup_data_frame(self, df: pd.DataFrame, config: MetricSummaryConfig):
        for (column, values) in config.filter.items():
            df = df.loc[~df[column].isin(values)] 
        return df    

    def _group_data_frame(self, df: pd.DataFrame, grouping_columns: Tuple[str]):
        columns = list(grouping_columns)
        if not columns:
            return df
        return df.groupby(columns)

    def _summarize_file(self, file_path: str, summary_config: MetricSummaryConfig) -> List:
        output = []
        data_frame = pd.read_csv(file_path)
        filtered_data_frame = self._cleanup_data_frame(data_frame, summary_config)
        for group in summary_config.groupby:
            grouped_data_frame = self._group_data_frame(filtered_data_frame, group)
            output.append(grouped_data_frame.describe(percentiles=[0.01, 0.5, 0.99])[summary_config.summary_columns])
        return output

confs = []
confs.append(MetricSummaryConfig("cassandra_disk_usage", groupby=[[], ["persistentvolumeclaim"]]))
confs.append(MetricSummaryConfig("cassandra_r_latency", groupby=[[], ["pod"]]))
confs.append(MetricSummaryConfig("cassandra_w_latency", groupby=[[], ["pod"]]))
confs.append(MetricSummaryConfig("cassandra_table_disk_space", groupby=[[], ["pod"]]))
confs.append(MetricSummaryConfig("cilrate_failures", groupby=[[], ["operation"]]))
confs.append(MetricSummaryConfig("cilrate_latency", groupby=[[], ["operation"]]))
confs.append(MetricSummaryConfig("cilrate_requests", groupby=[[], ["operation"]]))
confs.append(MetricSummaryConfig("overload_protection", groupby=[[], ["pod", "mechanism"]]))
confs.append(MetricSummaryConfig("compaction_data", groupby=[[], ["pod"]]))
confs.append(MetricSummaryConfig("container_cpu", filter={"container": ["stress-simulator"]}, groupby=[["pod"], ["container"]]))

summarizer = Summarizer(confs)
summarizer.summarize("/home/eourjoa/Desktop/PerformanceComparison/trial2/C4_singlesite_migrated/artifacts")