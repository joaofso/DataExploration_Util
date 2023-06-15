from summarize_results import MetricSummaryConfig, Summarizer


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
summarizer.summarize("./ext_resources")