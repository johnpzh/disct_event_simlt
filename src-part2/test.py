import os
import subprocess as sp
import numpy as np
import statistics as stat
from datetime import datetime
from datetime import timedelta
from rvgs import Exponential as Expo


def get_var_and_cv(trace_file):
    with open(trace_file) as trace:
        count = 0
        delay_times = list()
        for line in trace:
            attris = line.split()
            delay_t = float(attris[6])
            delay_times.append(delay_t)

        mean = stat.mean(delay_times)
        var = stat.pvariance(delay_times)
        stdev = stat.pstdev(delay_times)
        cv = stdev / mean
        print("Mean:", mean)
        print("Standard Deviation:", stdev)
        print("C.V.:", cv)

def test1():
    print("Origin:")
    trace_file = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time_depart/UCB-Trace-846890339-848409417.csv'
    get_var_and_cv(trace_file)
    print("Expo:")
    trace_file = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/expo_service_time_depart/UCB-Trace-846890339-848409417.csv'
    get_var_and_cv(trace_file)

if __name__ == '__main__':
    test1()
            