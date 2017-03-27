'''add the lag time to the trace'''
import os
import subprocess as sp
from datetime import datetime
from datetime import timedelta

def get_lag_time(trace_path, extracted):
    '''Calculate job delay time, 
    added to the trace to get a new trace file.'''
    with open(trace_path) as trace, \
        open(extracted, 'w') as output:
        # trace_new = list()
        count = 0
        for line in trace:
            attris = line.split()
            # Get job lag time (delay time)
            # print('attris: ', attris)#test
            arrival_time_ts = float(attris[0])
            end_time_ts = float(attris[2])
            lag_time = end_time_ts - arrival_time_ts
            attris.append(str(lag_time))
            new_line = ' '.join(attris) + '\n'
            output.write(new_line)
            # print('new_line', new_line)#test
            count += 1
            if count % 100000 == 0:
                print('.', end='', flush=True) 
        print('', flush=True)

def get_delay_time_mean(trace_path):
    '''Calculate mean job delay time'''
    with open(trace_path) as trace:
        delay_time = 0.0
        count = 0
        for line in trace:
            count += 1
            attris = line.split()
            dt = float(attris[6])
            delay_time += dt
            if count % 100000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)
        delay_time_mean = delay_time / count
        return delay_time_mean

def get_utilization(trace_path):
    '''Calculate system utilization, using every jobs' service time'''
    with open(trace_path) as trace:
        service_time = 0.0
        count = 0
        for line in trace:
            count += 1
            attris = line.split()
            if count == 1:
                # Arrival Time 1
                a_1 = float(attris[0])
            # Service Time
            st = float(attris[5])
            service_time += st
            if count % 100000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)

        a_n = float(attris[0])
        # arrival_rate = count / (a_n - a_1)
        # service_rate = count / service_time
        # util = arrival_rate / service_rate
        util = service_time / (a_n - a_1)
        return util

def get_total_service_time(trace_path):
    '''Calculate total service time'''
    with open(trace_path) as trace:
        count = 0
        service_process = list()
        for line in trace:
            attris = line.split()
            start_time = float(attris[1])
            end_time = float(attris[2])
            service_process.append([start_time, end_time])
        service_process.sort(key=lambda time:time[0])

        # Get all time ranges (periods)
        time_range = list()
        for start, end in service_process:
            if len(time_range) == 0:
                time_range.append([start, end])
                continue
            last_end = time_range[-1][1]
            if start < last_end and end > last_end:
                time_range[-1][1] = end # extend the range
            elif start > last_end:
                time_range.append([start, end])

        # Get the totla service time
        # print('time_range:', time_range)#test
        total_service_time = 0.0
        for start, end in time_range:
            total_service_time += end - start
        return total_service_time

def get_utilization_multi_servers(trace_path):
    '''Calculate system utilization, using 
    max(service end time) - min(service start time)'''
    with open(trace_path) as trace:
        count = 0
        service_start_time = datetime(1996, 11, 20).timestamp()
        service_end_time = 0
        for line in trace:
            count += 1
            attris = line.split()
            if count == 1:
                a_1 = float(attris[0])
            if count % 100000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)
        a_n = float(attris[0])
        # arrival_rate = count / (a_n - a_1)
        # service_rate = count / (service_end_time - service_start_time)
        # util = arrival_rate / service_rate
        # util = (service_end_time - service_start_time) / (a_n - a_1)
        total_service_time = get_total_service_time(trace_path)
        arrival_time_range = a_n - a_1
        util = total_service_time / arrival_time_range
        print('@131 total_service_time:', total_service_time)#test
        print('@32 arrival_time_range:', arrival_time_range)#test
        return util

def get_queue_length_mean(trace_path):
    '''Calculate mean queue length'''
    with open(trace_path) as trace:
        count = 0
        arrival_times = list()
        start_times = list()
        for line in trace:
            count += 1
            attris = line.split()
            at = float(attris[0])
            arrival_times.append(at)
            st = float(attris[1]) # Here the 1 is for waiting queue length
            # st = float(attris[2]) # Here the 2 is for system queue length
            start_times.append(st)
        start_times.sort()
        i = 0
        j = 0
        queue_lengths = list()
        time_q = arrival_times[i]
        i += 1
        length = 1
        while i != len(arrival_times) and j != len(start_times):
            if arrival_times[i] < start_times[j]:
                # length += 1
                # i += 1
                period = arrival_times[i] - time_q
                queue_lengths.append([length, period])
                time_q = arrival_times[i]
                length += 1
                i += 1
            elif start_times[j] < arrival_times[i]:
                period = start_times[j] - time_q
                queue_lengths.append([length, period])
                time_q = start_times[j]
                length -= 1
                j += 1
            else:
                i += 1
                j += 1
        while i != len(arrival_times):
            period = arrival_times[i] - time_q
            queue_lengths.append([length, period])
            time_q = arrival_times[i]
            length += 1
            i += 1
        while j != len(start_times):
            period = start_times[j] - time_q
            queue_lengths.append([length, period])
            time_q = start_times[j]
            length -= 1
            j += 1

        # Calculate the mean queue length
        period_total = 0.0
        length_v = 0.0
        for l, p in queue_lengths:
            length_v += l * p
            period_total += p
        result = length_v / period_total
        return result

def extract_single():
    # from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted/'
    file_name = 'UCB-Trace-846890339-848409417.csv'
    # file_name = 'UCB-Trace-846890339-848409417.csv'
    # trace_path = from_direct + file_name
    print('File:', file_name)

    # to_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/expo_service_time_depart/'
    to_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time_depart/'
    # to_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/expo_service_time/'
    extracted = to_direct + file_name
    # get_lag_time(trace_path, extracted)
    # for i in range(1, 11):
        # to_file_name = file_name[:-4] + '_{0:02d}.csv'.format(i)
        # extracted = to_direct + to_file_name

        # Mean Job delay time
    delay_time_mean = get_delay_time_mean(extracted)
    print('delay_time_mean:', delay_time_mean)

    # System utilization
    utilization = get_utilization(extracted)
    print('Utilization:', utilization)
    # util2 = get_utilization_multi_servers(extracted)
    # print('Util2:', util2)

    # Mean waiting queue length
    queue_length = get_queue_length_mean(extracted)
    print('Mean queue length:', queue_length)

        # result = [str(utilization), str(queue_length), str(delay_time_mean)]
        # line = ' '.join(result)
        # output.write(line + '\n')

def extract(output):
    # from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted/'
    file_name = 'UCB-Trace-846890339-848409417.csv'
    # file_name = 'UCB-Trace-846890339-848409417.csv'
    # trace_path = from_direct + file_name
    print('File:', file_name)

    # to_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/expo_service_time_depart/'
    to_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace2/delay_time_depart/'
    # to_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/expo_service_time/'
    # extracted = to_direct + file_name
    # get_lag_time(trace_path, extracted)
    for i in range(1, 6):
        to_file_name = file_name[:-4] + '_{0:02d}.csv'.format(i)
        extracted = to_direct + to_file_name

        # Mean Job delay time
        delay_time_mean = get_delay_time_mean(extracted)
        print('delay_time_mean:', delay_time_mean)

        # System utilization
        utilization = get_utilization(extracted)
        print('Utilization:', utilization)
        # util2 = get_utilization_multi_servers(extracted)
        # print('Util2:', util2)

        # Mean waiting queue length
        queue_length = get_queue_length_mean(extracted)
        print('Mean queue length:', queue_length)

        result = [str(utilization), str(queue_length), str(delay_time_mean)]
        line = ' '.join(result)
        output.write(line + '\n')
    


if __name__ == '__main__':
    extract_single()
    # output_file = 'outputs/expo_metrics_vs_util.txt'
    # output_file = 'outputs/origin_metrics_vs_util.txt'
    # with open(output_file, 'w') as output:
    #     extract(output)