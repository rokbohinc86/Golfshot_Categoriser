## Generate your data set

1) Import driving range sessions csv files into data/raw/Metrics
2) Import videos into data/raw/Videos
3) Rename metrics files in order to detect duplicates and to order them cronologically by running MetricsFileRenaming.py
4) Create a single metrics file by merging all metrics files together by running MetricsMerge.py
5) Create a data set for predicting shot type by running CreateDataSet.py