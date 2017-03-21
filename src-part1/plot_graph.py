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
    plt.ylim(0.140, 0.185)
    plt.xticks(np.arange(1, len(mean_list)+1, 1))
    plt.tick_params(direction='in')
    line1, = plt.plot(x, mean_list, label='Transient Mean')
    line2, = plt.plot([1, 19], \
                [0.17840999969378782, 0.17840999969378782], \
                'k--', \
                label='Mean')
    # plt.legend([line1, line2], ['Transient Mean', 'Mean'])
    fig_file = directory + 'iat_mean.pdf'
    plt.savefig(fig_file, format='pdf')
    # plt.show()

    plt.figure(2)
    plt.xlabel('Number of Days')
    plt.ylabel(r'Variance of Inter-arrival Time ($\mathrm{s}^2$)')
    plt.xlim(1, len(var_list))
    plt.ylim(0, 100)
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
    plt.ylim(0, 10)
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
    plt.ylim(0, 60)
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

    plt.figure(5)
    plt.xlabel('Number of Days')
    plt.ylabel('Mean of Service Time (s)')
    plt.xlim(1, len(mean_list))
    plt.ylim(14.75, 16.75)
    plt.xticks(np.arange(1, len(mean_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, mean_list)
    plt.plot([1, 19], [16.4128992069338, 16.4128992069338], 'k--')
    fig_file = directory + 'st_mean.pdf'
    plt.savefig(fig_file, format='pdf')
    # plt.show()

    plt.figure(6)
    plt.xlabel('Number of Days')
    plt.ylabel(r'Variance of Service Time ($\mathrm{s}^2$)')
    plt.xlim(1, len(var_list))
    plt.ylim(13000, 17000)
    plt.xticks(np.arange(1, len(var_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, var_list)
    plt.plot([1, 19], [16142.258468152095, 16142.258468152095], 'k--')
    fig_file = directory + 'st_var.pdf'
    plt.savefig(fig_file, format='pdf')

    plt.figure(7)
    plt.xlabel('Number of Days')
    plt.ylabel('Standard Deviation of Service Time (s)')
    plt.xlim(1, len(sd_list))
    plt.ylim(114, 130)
    plt.xticks(np.arange(1, len(sd_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, sd_list)
    plt.plot([1, 19], [127.0521879707394, 127.0521879707394], 'k--')
    fig_file = directory + 'st_sd.pdf'
    plt.savefig(fig_file, format='pdf')

    plt.figure(8)
    plt.xlabel('Number of Days')
    plt.ylabel('C.V. of Service Time')
    plt.xlim(1, len(cv_list))
    plt.ylim(7.50, 8)
    plt.xticks(np.arange(1, len(cv_list)+1, 1))
    plt.tick_params(direction='in')
    plt.plot(x, cv_list)
    plt.plot([1, 19], [7.740996052486868, 7.740996052486868], 'k--')
    fig_file = directory + 'st_cv.pdf'
    plt.savefig(fig_file, format='pdf')

def plot_iat_autocorr():
    # Inter-arrival time
    directory = 'outputs/'
    file_name = 'inter-arrival-time_autocorr.txt'
    path = directory + file_name
    with open(path) as input:
        for line in input:
            iat_acs = line.split()

    plt.figure(1)
    plt.xlabel('Lag')
    plt.ylabel('Sample Autocorrelation')
    plt.xlim(0, len(iat_acs))
    plt.ylim(0, 0.0007)
    # plt.xticks(np.arange(1, len(iat_acs)+1, 1))
    plt.tick_params(direction='in')
    x = np.arange(1, len(iat_acs)+1)
    line1, = plt.plot(x, iat_acs, '.')
    # line2, = plt.plot([1, 19], \
    #             [0.17840999969378782, 0.17840999969378782], \
    #             'k--', \
    #             label='Mean')
    # plt.legend([line1, line2], ['Transient Mean', 'Mean'])
    fig_file = directory + 'iat_autocorr.pdf'
    plt.savefig(fig_file, format='pdf')

def plot_st_autocorr():
    # Inter-arrival time
    directory = 'outputs/'
    file_name = 'service-time_autocorr.txt'
    path = directory + file_name
    with open(path) as input:
        for line in input:
            st_acs = line.split()

    plt.figure(2)
    plt.xlabel('Lag')
    plt.ylabel('Sample Autocorrelation')
    plt.xlim(0, len(st_acs))
    plt.ylim(-0.005, 0.035)
    # plt.xticks(np.arange(1, len(st_acs)+1, 1))
    plt.tick_params(direction='in')
    x = np.arange(1, len(st_acs)+1)
    line1, = plt.plot(x, st_acs, '.')
    # line2, = plt.plot([1, 19], \
    #             [0.17840999969378782, 0.17840999969378782], \
    #             'k--', \
    #             label='Mean')
    # plt.legend([line1, line2], ['Transient Mean', 'Mean'])
    fig_file = directory + 'st_autocorr.pdf'
    plt.savefig(fig_file, format='pdf')

if __name__ == '__main__':
    # plot_iat_metrics()
    # plot_st_metrics()
    plot_iat_autocorr()
    plot_st_autocorr()
