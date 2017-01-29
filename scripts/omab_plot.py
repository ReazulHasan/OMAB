#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pandas import DataFrame

__author__ = 'Bence Cserna'


def construct_data_frame(data):
    flat_data = [flatten(experiment) for experiment in data]
    return DataFrame(flat_data)


def regret_box_plot(experiments):
    boxplot = sns.boxplot(x="algorithm",
                          y="regret",
                          data=experiments,
                          showmeans=True)
    plt.show(boxplot)


def regret_plot(data):
    regret_series = data[['algorithm', 'cumSumRegrets']].groupby('algorithm').apply(list_average,
                                                                                    'cumSumRegrets')

    print(regret_series)
    values = []
    for row in regret_series.values:
        values.append([value for value in row])

    max_len = 0
    for row in values:
        max_len = max(len(row), max_len)

    # Fill missing values with NaN
    for row in values:
        if len(row) < max_len:
            row += [float('NaN')] * (max_len - len(row))

    frame = DataFrame(np.asarray(values).T, columns=list(regret_series.index))
    print(frame)
    # plt.figure()
    frame.plot()
    plt.show()


def read_data(file_name):
    with open(file_name) as file:
        content = json.load(file)
    return content


def list_average(group, key):
    return [sum(col) / float(len(col)) for col in zip(*group[key])]


def list_average_cum_sum(group, key):
    averages = [sum(col) / float(len(col)) for col in zip(*group[key])]
    cum_sums = [averages[x] * (1 + x) for x in range(len(averages))]

    return cum_sums


def configure_sns():
    sns.set_style("white")


def main():
    configure_sns()
    data = DataFrame(read_data("../results/resultT.dat"))
    print(data)
    # data2 = DataFrame(read_data("../results/result_rtdp_h80.dat"))
    # regret_box_plot(data)
    # data.set_index('algorithm', inplace=True)
    # data = data.append(data2, ignore_index=True)
    regret_plot(data)


if __name__ == "__main__":
    main()