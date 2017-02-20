'''Plot graph according to data'''
import numpy as np
import matplotlib.pyplot as plt

def plot_iat_metrics():

    # Inter-arrival time
    directory = 'outputs/'
    file_name = 'inter-arrival-time_metrics.txt'
    path = directory + file_name
    with open(path) as input:
        count = 0
        for line in input:
            count += 1
            if count == 1:
                x = line.split()
            elif count == 2:
                mean_list = line.split()
            elif count == 3:
                var_list = line.split()
            elif count == 4:
                sd_list = line.split()
            elif count == 5:
                cv_list = line.split()

    plt.figure(1)
    plt.xlabel('Number of Days')
    plt.ylabel('Mean of Inter-arrival Time (s)')
    plt.xlim(1, len(mean_list))
    plt.xticks(np.arange(1, len(mean_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, mean_list)
    plt.plot([1, 19], [0.17840999969378782, 0.17840999969378782], 'k--')
    fig_file = directory + 'iat_mean.pdf'
    plt.savefig(fig_file, format='pdf')
    # plt.show()

    plt.figure(2)
    plt.xlabel('Number of Days')
    plt.ylabel(r'Variance of Inter-arrival Time ($\mathrm{s}^2$)')
    plt.xlim(1, len(var_list))
    plt.xticks(np.arange(1, len(var_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, var_list)
    plt.plot([1, 19], [93.54184330347893, 93.54184330347893], 'k--')
    fig_file = directory + 'iat_var.pdf'
    plt.savefig(fig_file, format='pdf')

    plt.figure(3)
    plt.xlabel('Number of Days')
    plt.ylabel('Standard Deviation of Inter-arrival Time (s)')
    plt.xlim(1, len(sd_list))
    plt.xticks(np.arange(1, len(sd_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, sd_list)
    plt.plot([1, 19], [9.671703226602796, 9.671703226602796], 'k--')
    fig_file = directory + 'iat_sd.pdf'
    plt.savefig(fig_file, format='pdf')

    plt.figure(4)
    plt.xlabel('Number of Days')
    plt.ylabel('C.V. of Inter-arrival Time')
    plt.xlim(1, len(cv_list))
    plt.xticks(np.arange(1, len(cv_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, cv_list)
    plt.plot([1, 19], [54.21054449415798, 54.21054449415798], 'k--')
    fig_file = directory + 'iat_cv.pdf'
    plt.savefig(fig_file, format='pdf')

def plot_st_metrics():

    # Inter-arrival time
    directory = 'outputs/'
    file_name = 'service-time_metrics.txt'
    path = directory + file_name
    with open(path) as input:
        count = 0
        for line in input:
            count += 1
            if count == 1:
                x = line.split()
            elif count == 2:
                mean_list = line.split()
            elif count == 3:
                var_list = line.split()
            elif count == 4:
                sd_list = line.split()
            elif count == 5:
                cv_list = line.split()

    plt.figure(1)
    plt.xlabel('Number of Days')
    plt.ylabel('Mean of Service Time (s)')
    plt.xlim(1, len(mean_list))
    plt.xticks(np.arange(1, len(mean_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, mean_list)
    plt.plot([1, 19], [16.4128992069338, 16.4128992069338], 'k--')
    fig_file = directory + 'st_mean.pdf'
    plt.savefig(fig_file, format='pdf')
    # plt.show()

    plt.figure(2)
    plt.xlabel('Number of Days')
    plt.ylabel(r'Variance of Service Time ($\mathrm{s}^2$)')
    plt.xlim(1, len(var_list))
    plt.xticks(np.arange(1, len(var_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, var_list)
    plt.plot([1, 19], [16142.258468152095, 16142.258468152095], 'k--')
    fig_file = directory + 'st_var.pdf'
    plt.savefig(fig_file, format='pdf')

    plt.figure(3)
    plt.xlabel('Number of Days')
    plt.ylabel('Standard Deviation of Service Time (s)')
    plt.xlim(1, len(sd_list))
    plt.xticks(np.arange(1, len(sd_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, sd_list)
    plt.plot([1, 19], [127.0521879707394, 127.0521879707394], 'k--')
    fig_file = directory + 'st_sd.pdf'
    plt.savefig(fig_file, format='pdf')

    plt.figure(4)
    plt.xlabel('Number of Days')
    plt.ylabel('C.V. of Service Time')
    plt.xlim(1, len(cv_list))
    plt.xticks(np.arange(1, len(cv_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, cv_list)
    plt.plot([1, 19], [7.740996052486868, 7.740996052486868], 'k--')
    fig_file = directory + 'st_cv.pdf'
    plt.savefig(fig_file, format='pdf')

if __name__ == '__main__':
    # plot_iat_metrics()
    plot_st_metrics()