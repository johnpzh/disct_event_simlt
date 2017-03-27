'''Fitting the inter-arrival times and service times,
plot figures and calculate goodness'''
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import statistics as stat
import math

FIGURE_COUNT = 0

def fitting_pdf(data, x_label, output_file):
    print('PDF fitting:')
    global FIGURE_COUNT
    FIGURE_COUNT += 1 
    plt.figure(FIGURE_COUNT)
    plt.xlabel(x_label)
    count = len(data)
    # print('count:', count)#test
    k = math.floor(1 + math.log(count, 2))
    # k = 100
    n, bins, patches = plt.hist(data, k, normed=True, edgecolor='k')
    # cdf = np.cumsum(n)
    # print('@21 cdf:', cdf)#test
    xs = list()
    for i in range(len(bins) - 1):
        x = (bins[i+1] + bins[i])/2
        xs.append(x)
    # print('n:', n)#test
    # print('bins:', bins)#test
    plt.tick_params(direction='in')
    # Fitting distribution
    distributions = ['expon', 'norm', 'lognorm']
    for dist_name in distributions:
        dist = getattr(st, dist_name)
        params = dist.fit(data)
        # params = dist.fit(n)
        pdf_fitted = dist.pdf(xs, loc=params[-2], \
                            scale=params[-1], *params[:-2])
        plt.plot(xs, pdf_fitted, label=dist_name)
        sse = np.sum(np.power(n - pdf_fitted, 2.0))
        print(dist_name, 'sse:', sse)
        print('loc:', params[-2], 'scale:', params[-1])
    plt.legend()
    plt.savefig(output_file, format='pdf')

def fitting_cdf(data, x_label, output_file):
    print('CDF fitting:')
    # Inter-arrival time
    global FIGURE_COUNT
    FIGURE_COUNT += 1 
    plt.figure(FIGURE_COUNT)
    plt.xlabel(x_label)
    plt.ylabel('CDF')
    plt.tick_params(direction='in')

    k = 1000
    counts, bins = np.histogram(data, bins=k, density=True)
    # print('counts:', counts)#test
    cdf = np.cumsum(counts) * (bins[1] - bins[0])
    # print('cdf:', cdf)#test
    xs = bins[1:]
    plt.plot(xs, cdf, label='Original')

    distributions = ['expon', 'norm', 'lognorm']
    for dist_name in distributions:
        dist = getattr(st, dist_name)
        params = dist.fit(data)
        # params = dist.fit(n)

        cdf_fitted = dist.cdf(xs, loc=params[-2], \
                            scale=params[-1], *params[:-2])
        # print('cdf_fitted[-1]:', cdf_fitted[-1])#test
        plt.plot(xs, cdf_fitted, label=dist_name)
        sse = np.sum(np.power(cdf - cdf_fitted, 2.0))
        print(dist_name, 'sse:', sse)
        print('loc:', params[-2], 'scale:', params[-1])
    plt.legend()
    plt.savefig(output_file, format='pdf')
    # print('CDF[-1]:', cdf[-1])#test




def get_data(trace_path):
    # get inter-arrival times and  service times
    with open(trace_path) as trace:
        inter_arrival_times = list()
        service_times = list()
        count = 0
        i_a_t_lower = 5.08870900e+00
        # i_a_t_upper = 5.01322760e+03
        # i_a_t_upper = 1512.29904194
        # i_a_t_upper = 282.84943343
        i_a_t_upper = 108.04320912
        # i_a_t_upper = 57.01389575

        s_t_lower = 1.30000000e-05
        # s_t_upper = 1.14368168e+03
        # s_t_upper = 1.40708918e+02
        s_t_upper = 1.05343289e+02
        # s_t_upper = 4.60010958e+01
        # s_t_upper = 5.25726790e+01
        # s_t_upper = 2.58740933e+01
        for line in trace:
            count += 1
            attris = line.split()
            i_a_time = float(attris[4])
            s_time = float(attris[5])
            if not (i_a_time >= i_a_t_lower \
                and i_a_time < i_a_t_upper \
                and s_time >= s_t_lower \
                and s_time < s_t_upper):
                continue
            if count != 1:
                inter_arrival_times.append(i_a_time)
            service_times.append(s_time)


    i_a_time_mean = stat.mean(inter_arrival_times)
    i_a_time_stdev = stat.pstdev(inter_arrival_times)

    s_time_mean = stat.mean(service_times)
    s_time_stdev = stat.pstdev(service_times)

    print('i_a_time_mean:', i_a_time_mean, 'stdev:', i_a_time_stdev)
    print('s_time_mean:', s_time_mean, 'stdev:', s_time_stdev)

    # Inter-arrival Times
    output_file = 'outputs/inter_arrival_time_fit_pdf.pdf'
    x_label = 'Inter-arrival Times'
    fitting_pdf(inter_arrival_times, x_label, output_file)

    output_file = 'outputs/inter_arrival_time_fit_cdf.pdf'
    # fitting_cdf(inter_arrival_times, x_label, output_file)

    # Service Times
    output_file = 'outputs/service_time_fit_pdf.pdf'
    x_label = 'Service Times'
    fitting_pdf(service_times, x_label, output_file)

    output_file = 'outputs/service_time_fit_cdf.pdf'
    # fitting_cdf(service_times, x_label, output_file)

if __name__ == '__main__':
    from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time_depart/'
    file_name = 'UCB-Trace-846890339-848409417.csv'
    trace_path = from_direct + file_name

    get_data(trace_path)



