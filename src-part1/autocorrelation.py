'''Calculate the sample autocorrelation'''
from datetime import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
from save_list import save_list

def get_autocorrelation(trace_path):
    J_MAX = 1000
    directory = 'outputs/'
    iat_file = directory + 'inter-arrival-time_autocorr.txt'
    st_file = directory + 'service-time_autocorr.txt'
    with open(trace_path) as trace, \
        open(iat_file, 'w') as iat_output, \
        open(st_file, 'w') as st_output:
        iats = list()
        sts = list()
        count = 0
        for line in trace:
            count += 1
            attrts = line.split()
            interarrvl_t = float(attrts[-2])
            service_t = float(attrts[-1])
            if count != 1:
                iats.append(interarrvl_t)
            sts.append(service_t)

            if count % 1000000 == 0:
                print('.', end='', flush=True)
        print('count:', count)

        # Inter-arrival time
        print('Inter-arrival Time')
        iat_n = len(iats)
        iat_mean = sum(iats) / iat_n
        iat_v = 0
        count = 0
        for iat in iats:
            count += 1
            iat_v += (iat - iat_mean)**2
            if count % 1000000 == 0:
                print('.', end='', flush=True)
        print()
        iat_var = iat_v / iat_n

        c0 = iat_var
        iat_acs = list()
        for j in range(1, J_MAX + 1):
            cj_v = 0
            for i in range(0, iat_n - j):
                cj_v += (iats[i] - iat_mean)*(iats[i+j] - iat_mean)
            cj = cj_v / (iat_n - j)
            rj = cj / c0
            iat_acs.append(str(rj))
            print('.', end='', flush=True)
        print()
        line = ' '.join(iat_acs) + '\n'
        iat_output.write(line)

        # Service time
        print('Service Time')
        st_n = len(sts)
        st_mean = sum(sts) / st_n
        st_v = 0
        count = 0
        for st in sts:
            count += 1
            st_v += (st - st_mean)**2
            if count % 1000000 == 0:
                print('.', end='', flush=True)
        print()
        st_var = st_v / st_n

        c0 = st_var
        st_acs = list()
        for j in range(1, J_MAX + 1):
            cj_v = 0
            for i in range(0, st_n - j):
                cj_v += (sts[i] - st_mean)*(sts[i+j] - st_mean)
            cj = cj_v / (st_n - j)
            rj = cj / c0
            st_acs.append(str(rj))
            print('.', end='', flush=True)
        print()
        line = ' '.join(st_acs) + '\n'
        st_output.write(line)
    pass

if __name__ == '__main__':
    # All trace
    directory = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted/'
    file_name = 'UCB-Trace-846890339-848409417.csv'

    # First part
    # directory = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted/'
    # file_name = 'UCB-home-IP-846890339-847313219.csv'

    # Little sample
    # directory = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/sample/'
    # file_name = 'examples_times.csv'
    trace_path = directory + file_name

    get_autocorrelation(trace_path)