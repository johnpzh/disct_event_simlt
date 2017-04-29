'''Plot graph according to data'''
import numpy as np
import matplotlib.pyplot as plt

FIGURE_COUNT = 0

def plot_iat_autocorr(record_file, fig_file):
    # Inter-arrival time
    with open(record_file) as input:
        for line in input:
            iat_acs = line.split()
    global FIGURE_COUNT
    plt.figure(FIGURE_COUNT)
    FIGURE_COUNT += 1
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation of Inter-arrival Time')
    plt.xlim(0, len(iat_acs))
    # plt.ylim(0, 0.0007)
    # plt.xticks(np.arange(1, len(iat_acs)+1, 1))
    plt.tick_params(direction='in')
    x = np.arange(1, len(iat_acs)+1)
    line1, = plt.plot(x, iat_acs, '.', clip_on=False)
    # line2, = plt.plot([1, 19], \
    #             [0.17840999969378782, 0.17840999969378782], \
    #             'k--', \
    #             label='Mean')
    # plt.legend([line1, line2], ['Transient Mean', 'Mean'])
    plt.savefig(fig_file, format='pdf')

def main():
    record_file = 'outputs/autocor_sjf.txt'
    fig_file = 'outputs/autocor_sjf.pdf'
    plot_iat_autocorr(record_file, fig_file)

    record_file = 'outputs/autocor_fifo.txt'
    fig_file = 'outputs/autocor_fifo.pdf'
    plot_iat_autocorr(record_file, fig_file)

    

if __name__ == '__main__':
    main()
