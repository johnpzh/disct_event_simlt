'''add the lag time to the trace'''
import os
import subprocess as sp
from datetime import datetime
from datetime import timedelta

def get_lag_time(trace_path, extracted):
    with open(trace_path) as trace, \
        open(extracted, 'w') as output:
        trace_new = list()
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
    with open(trace_path) as trace:
        delay_time = 0.0
        count = 0
        for line in trace:
            count += 1
            attris = line.split()
            dt = float(attris[-1])
            delay_time += dt
            if count % 100000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)
        delay_time_mean = delay_time / count
        return delay_time_mean

def get_utilization(trace_path):
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

def get_utilization_multi_servers(trace_path):
    with open(trace_path) as trace:
        count = 0
        service_start_time = datetime(1996, 11, 20).timestamp()
        service_end_time = 0
        for line in trace:
            count += 1
            attris = line.split()
            if count == 1:
                a_1 = float(attris[0])
            st = float(attris[1])
            et = float(attris[2])
            if st < service_start_time:
                service_start_time = st
            if et > service_end_time:
                service_end_time = et
            if count % 100000 == 0:
                print('.', end='', flush=True)
        print('', flush=True)
        a_n = float(attris[0])
        # arrival_rate = count / (a_n - a_1)
        # service_rate = count / (service_end_time - service_start_time)
        # util = arrival_rate / service_rate
        util = (service_end_time - service_start_time) / (a_n - a_1)
        return util

def get_utilization_multi_servers_time(trace_path):
    pass

def get_queue_length_mean(trace_path):
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

def extract():
    # from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/sample/'
    # file_name = 'examples_times.csv'

    from_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted/'
    file_name = 'UCB-Trace-846890339-848409417.csv'
    trace_path = from_direct + file_name

    # to_direct = '/Users/johnz/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted_lag_time/'
    to_direct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted_lag_time/'
    extracted = to_direct + file_name
    # get_lag_time(trace_path, extracted)

    # Mean Job delay time
    # delay_time_mean = get_delay_time_mean(extracted)
    # print('delay_time_mean:', delay_time_mean)

    # System utilization
    # utilization = get_utilization(extracted)
    # print('Utilization:', utilization)
    # util2 = get_utilization_multi_servers(extracted)
    # print('Util2:', util2)

    # Mean waiting queue length
    queue_length = get_queue_length_mean(extracted)
    print('Mean queue length:', queue_length)


if __name__ == '__main__':
    extract()