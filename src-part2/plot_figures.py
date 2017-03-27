'''Plot figures'''
import numpy as np
import matplotlib.pyplot as plt

FIGURE_COUNT = 0

def plot_idt_autocor(input_file, output_file):
    with open(input_file) as input:
        for line in input:
            inter_depart_times = line.split()
            break
    global FIGURE_COUNT
    FIGURE_COUNT += 1
    plt.figure(FIGURE_COUNT)
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation of Departure Process')
    plt.xlim(0, len(inter_depart_times))
    # plt.ylim(0, 0.0009)
    # plt.xticks(np.arange(1, len(inter_depart_times)+1, 1))
    plt.tick_params(direction='in')
    x = np.arange(1, len(inter_depart_times)+1)
    line1, = plt.plot(x, inter_depart_times, '.', clip_on=False)
    # line2, = plt.plot([1, 19], \
    #             [0.17840999969378782, 0.17840999969378782], \
    #             'k--', \
    #             label='Mean')
    # plt.legend([line1, line2], ['Transient Mean', 'Mean'])
    # fig_file = directory + 'iat_autocorr.pdf'
    plt.savefig(output_file, format='pdf')

def plot_metrics_vs_util():
    input_file = 'outputs/origin_metrics_vs_util.txt'
    with open(input_file) as input:
        utils_origin = list()
        queue_lens_origin = list()
        delay_times_origin = list()
        for line in input:
            attris = line.split()
            utils_origin.append(float(attris[0]))
            queue_lens_origin.append(float(attris[1]))
            delay_times_origin.append(float(attris[2]))

    input_file = 'outputs/expo_metrics_vs_util.txt'
    with open(input_file) as input:
        utils_expo = list()
        queue_lens_expo = list()
        delay_times_expo = list()
        for line in input:
            attris = line.split()
            utils_expo.append(float(attris[0]))
            queue_lens_expo.append(float(attris[1]))
            delay_times_expo.append(float(attris[2]))

    global FIGURE_COUNT

    # Mean Waiting Queue Length
    output_file = 'outputs/queue_len_vs_util.pdf'
    FIGURE_COUNT += 1
    plt.figure(FIGURE_COUNT)
    plt.xlabel('System Utilization')
    plt.ylabel('Mean Watiting Queue Length')
    plt.xlim(0.1, 0.9)
    # plt.ylim(0, 0.0009)
    plt.xticks(np.linspace(0.1, 0.9, 5))
    plt.tick_params(direction='in')
    # x = np.arange(1, len(inter_depart_times)+1)
    line1, = plt.plot(utils_origin, queue_lens_origin, 'o-', \
                        label='Original', clip_on=False)
    line2, = plt.plot(utils_expo, queue_lens_expo, 'v--', \
                        label='Expoential', clip_on=False)
    plt.legend()
    plt.savefig(output_file, format='pdf')

    # Mean job delay time
    output_file = 'outputs/delay_time_vs_util.pdf'
    FIGURE_COUNT += 1
    plt.figure(FIGURE_COUNT)
    plt.xlabel('System Utilization')
    plt.ylabel('Mean Job Delay Time (s)')
    plt.xlim(0.1, 0.9)
    # plt.ylim(0, 0.0009)
    plt.xticks(np.linspace(0.1, 0.9, 5))
    plt.tick_params(direction='in')
    # x = np.arange(1, len(inter_depart_times)+1)
    line1, = plt.plot(utils_origin, delay_times_origin, 'o-', \
                        label='Original', clip_on=False)
    line2, = plt.plot(utils_expo, delay_times_expo, 'v--', \
                        label='Expoential', clip_on=False)
    plt.legend()
    plt.savefig(output_file, format='pdf')

def plot_multi_autocor_departure():
    global FIGURE_COUNT
    x = np.arange(1, 51)
    # Original Trace
    FIGURE_COUNT += 1
    plt.figure(FIGURE_COUNT)
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation of Departure Process')
    plt.xlim(0, 50)
    # plt.ylim(0, 0.0009)
    # plt.xticks(np.linspace(0.1, 0.9, 5))
    plt.tick_params(direction='in')
    input_file = 'outputs/origin_depart_autocor.txt'
    with open(input_file) as input:
        count = 0
        for line in input:
            count += 1
            y = line.split()
            if count == 1:
                plt.plot(x, y, 'o-', label=r'UTIL$\approx 0.1$', clip_on=False)
            elif count == 2:
                plt.plot(x, y, 'v--', label=r'UTIL$\approx 0.3$', clip_on=False)
            elif count == 3:
                plt.plot(x, y, '^-.', label=r'UTIL$\approx 0.5$', clip_on=False)
            elif count == 4:
                plt.plot(x, y, '<:', label=r'UTIL$\approx 0.7$', clip_on=False)
            elif count == 5:
                plt.plot(x, y, '>-', label=r'UTIL$\approx 0.9$', clip_on=False)
    plt.legend()
    output_file = 'outputs/origin_depart_autocor.pdf'
    plt.savefig(output_file, format='pdf')

    # Exponential Trace
    FIGURE_COUNT += 1
    plt.figure(FIGURE_COUNT)
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation of Departure Process')
    plt.xlim(0, 50)
    # plt.ylim(0, 0.0009)
    # plt.xticks(np.linspace(0.1, 0.9, 5))
    plt.tick_params(direction='in')
    input_file = 'outputs/expo_depart_autocor.txt'
    with open(input_file) as input:
        count = 0
        for line in input:
            count += 1
            y = line.split()
            if count == 1:
                plt.plot(x, y, 'o-', label=r'UTIL$\approx 0.1$', clip_on=False)
            elif count == 2:
                plt.plot(x, y, 'v--', label=r'UTIL$\approx 0.3$', clip_on=False)
            elif count == 3:
                plt.plot(x, y, '^-.', label=r'UTIL$\approx 0.5$', clip_on=False)
            elif count == 4:
                plt.plot(x, y, '<:', label=r'UTIL$\approx 0.7$', clip_on=False)
            elif count == 5:
                plt.plot(x, y, '>-', label=r'UTIL$\approx 0.9$', clip_on=False)
    plt.legend()
    output_file = 'outputs/expo_depart_autocor.pdf'
    plt.savefig(output_file, format='pdf')


def main():
    from_direct = 'outputs/'
    file_name = 'inter-depart_time_autocor.txt'
    input_file = from_direct + file_name

    to_direct = from_direct
    file_name = 'inter-depart_time_autocor.pdf'
    output_file = to_direct + file_name

    # Inter-departure time autocorrelation
    # plot_idt_autocor(input_file, output_file)

    file_name = 'inter-depart_time_autocor_expo.txt'
    input_file = from_direct + file_name
    file_name = 'inter-depart_time_autocor_expo.pdf'
    output_file = to_direct + file_name
    # plot_idt_autocor(input_file, output_file)


    # Mean waiting Queue length and Mean delay times vs. System Utilization
    # plot_metrics_vs_util()

    # Inter-departure time autocorrelation of 5 different new traces
    plot_multi_autocor_departure()


if __name__ == '__main__':
    main()