'''Calculate the histogram of inter-arrival time and service time'''
from datetime import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
from save_list import save_list

def plot_iat_hist(iats, file_name):
    '''Plot Histogram of Inter-arrival Time'''
    plt.figure(1)
    count = len(iats)
    x = iats
    k = math.floor(1 + math.log(count, 2))
    # k = math.floor(count**0.5)
    # k = 10
    n, bins, patches = plt.hist(x, k, normed=True, edgecolor='k')
    # print('n:', n)#test
    # print('bins:', bins)#test
    # plt.ylim(0, 0.0010)
    plt.tick_params(direction='in')
    legend = mpatches.Patch(label=r'$k$='+str(k))
    plt.legend(handles=[legend], markerscale=0)
    plt.xlabel('Inter-arrivale Time')
    directory = 'outputs/'
    fig_file =  directory + file_name
    plt.savefig(fig_file, format='pdf')

def plot_st_hist(sts, file_name):
    '''Plot Histogram of Service Time'''
    plt.figure(2)
    count = len(sts)
    x = sts
    k = math.floor(1 + math.log(count, 2))
    # k = math.floor(count**0.5)
    # k = 10
    n, bins, patches = plt.hist(x, k, normed=True, edgecolor='k')
    # print('n:', n)#test
    # print('bins:', bins)#test
    # plt.ylim(0, 0.0018)
    plt.tick_params(direction='in')
    legend = mpatches.Patch(label=r'$k$='+str(k))
    plt.legend(handles=[legend])
    plt.xlabel('Service Time')
    directory = 'outputs/'
    fig_file =  directory + file_name
    plt.savefig(fig_file, format='pdf')

def plot_iat_cdf(iats, file_name):
    '''Plot Histogram of Inter-arrival Time'''
    plt.figure(1)
    # count = len(iats)
    # x = iats
    # x_lower = math.floor(min(iats))
    # x_upper = math.ceil(max(iats))
    # x = np.arange(x_lower, x_upper+1, 0.01)
    # y = np.cumsum(iats)
    # k = math.floor(1 + math.log(count, 2))
    # k = math.floor(count**0.5)
    # k = 10
    # n, bins, patches = plt.hist(x, k, normed=True, edgecolor='k')
    # n, bins, patches = plt.hist(x, k, normed=True, edgecolor='k', \
    #                             histtype='step', cumulative=True)
    x = sorted(iats)
    n = len(x)
    y = np.ones(n)
    y = np.cumsum(y)/n
    plt.plot(x, y)
    plt.ylim(0, 1)
    plt.tick_params(direction='in')
    plt.xlabel('Inter-arrivale Time')
    directory = 'outputs/'
    fig_file =  directory + file_name
    plt.savefig(fig_file, format='pdf')

def plot_st_cdf(sts, file_name):
    '''Plot Histogram of Service Time'''
    plt.figure(2)
    # count = len(sts)
    # x = sts
    # k = math.floor(1 + math.log(count, 2))
    # k = math.floor(count**0.5)
    # k = 10
    # n, bins, patches = plt.hist(x, k, normed=True, edgecolor='k')
    # n, bins, patches = plt.hist(x, k, normed=True, edgecolor='k', \
    #                             histtype='step', cumulative=True)
    # print('n:', n)#test
    # print('bins:', bins)#test
    # plt.ylim(0, 0.0018)
    x = sorted(sts)
    n = len(x)
    y = np.ones(n)
    y = np.cumsum(y)/n
    plt.plot(x, y)
    plt.ylim(0, 1)
    plt.tick_params(direction='in')
    plt.xlabel('Service Time')
    directory = 'outputs/'
    fig_file =  directory + file_name
    plt.savefig(fig_file, format='pdf')

def get_histogram_all(trace_path):
    with open(trace_path) as trace:
        interarrvl_ts = list()
        service_ts = list()
        count = 0
        for line in trace:
            count += 1
            attrts = line.split()
            interarrvl_t = float(attrts[-2])
            service_t = float(attrts[-1])
            if count != 1:
                interarrvl_ts.append(interarrvl_t)
            service_ts.append(service_t)

        # Inter-arrival Times
        plot_iat_hist(interarrvl_ts, 'iat_hist.pdf')

        # Service Times
        plot_st_hist(service_ts, 'st_hist.pdf')

def get_histogram_main(trace_path):
    with open(trace_path) as trace:
        interarrvl_ts = list()
        service_ts = list()
        count = 0
        iat_lower = 9.00000000e-05
        # iat_upper = 1.10977648e+03
        # iat_upper = 1.86117390e+01
        # iat_upper = 1.51527292e+00
        iat_upper = 7.24752217e-01

        st_lower = 5.00000000e-06
        # st_upper = 3.59823358e+03
        # st_upper = 1.49874819e+02
        # st_upper = 1.87343516e+01
        st_upper = 1.71052583e+01
        for line in trace:
            attrts = line.split()
            interarrvl_t = float(attrts[-2])
            service_t = float(attrts[-1])
            if not (interarrvl_t >= iat_lower \
                and interarrvl_t < iat_upper \
                and service_t >= st_lower \
                and service_t < st_upper):
                continue
            interarrvl_ts.append(interarrvl_t)
            service_ts.append(service_t)
            count += 1

            if count % 1000000 == 0:
                print('.', end='', flush=True)
        print('count:', count)
        # Inter-arrival Times
        # plot_iat_hist(interarrvl_ts, 'iat_hist_main.pdf')
        plot_iat_cdf(interarrvl_ts, 'iat_cdf_main.pdf')

        # Service Times
        # plot_st_hist(service_ts, 'st_hist_main.pdf')
        plot_st_cdf(service_ts, 'st_cdf_main.pdf')

def get_cdf_main(trace_path):
    with open(trace_path) as trace:
        interarrvl_ts = list()
        service_ts = list()
        count = 0
        for line in trace:
            count += 1
            attrts = line.split()
            interarrvl_t = float(attrts[-2])
            service_t = float(attrts[-1])
            if count != 1:
                interarrvl_ts.append(interarrvl_t)
            service_ts.append(service_t)

            if count % 1000000 == 0:
                print('.', end='', flush=True)
        print('count:', count)
        # Inter-arrival Times
        # plot_iat_cdf(interarrvl_ts, 'iat_cdf_main.pdf')
        plot_iat_cdf(interarrvl_ts, 'iat_cdf.pdf')

        # Service Times
        # plot_st_cdf(service_ts, 'st_cdf_main.pdf')
        plot_st_cdf(service_ts, 'st_cdf.pdf')

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
    # get_histogram_all(trace_path)
    # get_histogram_main(trace_path)
    get_cdf_main(trace_path)
