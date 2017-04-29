'''Calculate the steady-state values'''
import os
import subprocess as sp
import numpy as np
import heapq as hq
import statistics as stat
import scipy.stats as ss
from datetime import datetime
from datetime import timedelta

K = 64
B = 1024

class Metirc:
    def __init__(self):
        self.delay = 0
        self.wait = 0
        self.service = 0 
        self.server_queue = 0
        self.wait_queue = 0
        self.system_queue = 0

    def __str__(self):
        line = "delay: {}\n".format(self.delay)
        line += "wait: {}\n".format(self.wait)
        line += "service: {}\n".format(self.service)
        line += "server_queue: {}\n".format(self.server_queue)
        line += "wait_queue: {}\n".format(self.wait_queue)
        line += "system_queue: {}".format(self.system_queue)
        return line

RESULT = Metirc()

# def do_queue_length(arrivals, departures, period_range, start_length):
def do_queue_length(arrivals, departures, period_range):

    '''Generic function to calculate queue length'''
    i = 0
    j = 0
    queue_lengths = list()
    time_q = arrivals[0]
    i += 1
    length = 1
    # length = 1 + start_length
    while i < len(arrivals) and j < len(departures):
        if arrivals[i] < departures[j]:
            period = arrivals[i] - time_q
            queue_lengths.append([length, period])
            time_q = arrivals[i]
            length += 1
            i += 1
        elif departures[j] < arrivals[i]:
            period = departures[j] - time_q
            queue_lengths.append([length, period])
            time_q = departures[j]
            length -= 1
            j += 1
        else:
            i += 1
            j += 1
    while j < len(departures):
        period = departures[j] - time_q
        queue_lengths.append([length, period])
        time_q = departures[j]
        length -= 1
        j += 1

    # Calculate the mean queue length
    # period_total = 0.0
    length_v = 0.0
    for l, p in queue_lengths:
        # period_total += p
        length_v += l * p
    # result = length_v / period_total
    result = length_v / period_range
    # print('period_total:', period_total, 'period_range:', period_range)#test
    return result

# def system_queue_length(arrival_times, end_times):
#     i = 0
#     j = 0

# def get_server_queue_length(start_times, end_times, period_range, start_length):
#     return do_queue_length(start_times, end_times, period_range, start_length)

# def get_wait_queue_length(arrival_times, start_times, period_range, start_length):
#     return do_queue_length(arrival_times, start_times, period_range, start_length)

# def get_system_queue_length(arrival_times, end_times, period_range, start_length):
#     return do_queue_length(arrival_times, end_times, period_range, start_length)
def get_server_queue_length(start_times, end_times, period_range):
    return do_queue_length(start_times, end_times, period_range)

def get_wait_queue_length(arrival_times, start_times, period_range):
    return do_queue_length(arrival_times, start_times, period_range)

def get_system_queue_length(arrival_times, end_times, period_range):
    return do_queue_length(arrival_times, end_times, period_range)

def get_queue_lengths_batches(trace_file):
    '''Get the (wait, service, and system) queue lengths'''
    global RESULT
    global B
    global K
    with open(trace_file) as trace:
        # service_time = 0.0 #test
        # batches = list()
        server_queue_batchs = list()
        wait_queue_batchs = list()
        system_queue_batchs = list()

        count = 0
        arrival_times = list()
        start_times = list()
        end_times = list()
        for line in trace:
            bt = list()
            
            attris = line.split()
            arv_t = float(attris[0])
            arrival_times.append(arv_t)
            stt_t = float(attris[2])
            start_times.append(stt_t)
            end_t = float(attris[3])
            end_times.append(end_t)
            # queue = int(attris[6])
            # if count % B == 0:
            #     start_length = queue
            #     print('cout:', count) #test
            #     print('@131 start_length:', start_length) #test

            if count % B == B - 1:
                arrival_times.sort()
                start_times.sort()
                end_times.sort()
                period_range = end_times[-1] - arrival_times[0]

                server_queue = get_server_queue_length( \
                    start_times, end_times, period_range)
                    # start_times, end_times, period_range, 0)
                server_queue_batchs.append(server_queue)
                wait_queue = get_wait_queue_length( \
                    arrival_times, start_times, period_range)
                    # arrival_times, start_times, period_range, start_length)
                wait_queue_batchs.append(wait_queue)
                system_queue = get_system_queue_length( \
                    arrival_times, end_times, period_range)
                    # arrival_times, end_times, period_range, start_length)
                system_queue_batchs.append(system_queue)

                arrival_times.clear()
                start_times.clear()
                end_times.clear()
            count += 1
        # print('@155 len(system_queue_batchs):', len(system_queue_batchs))#test
        server_queue_mean = stat.mean(server_queue_batchs)
        wait_queue_mean = stat.mean(wait_queue_batchs)
        system_queue_mean = stat.mean(system_queue_batchs)

        RESULT.server_queue = server_queue_mean
        RESULT.wait_queue = wait_queue_mean
        RESULT.system_queue = system_queue_mean

        alpha = 0.05
        k = K
        df = k - 1
        t_value = ss.t.ppf(1 - alpha/2, df)

        server_queue_stdev = stat.pstdev(server_queue_batchs)
        endpoint_server_queue = t_value * server_queue_stdev/(k - 1)**0.5
        wait_queue_stdev = stat.pstdev(wait_queue_batchs)
        endpoint_wait_queue = t_value * wait_queue_stdev/(k - 1)**0.5
        system_queue_stdev = stat.pstdev(system_queue_batchs)
        endpoint_system_queue = t_value * system_queue_stdev/(k - 1)**0.5

        print('endpoint_server_queue:', endpoint_server_queue)
        print('endpoint_wait_queue:', endpoint_wait_queue)
        print('endpoint_system_queue:', endpoint_system_queue)

        # print('server_queue:', server_queue_mean)
        # print('wait_queue:', wait_queue_mean)
        # print('system_queue:', system_queue_mean)

def get_queue_lengths_whole(trace_file):
    '''Get the (wait, service, and system) queue lengths'''
    global RESULT
    global B
    global K
    with open(trace_file) as trace:
        # service_time = 0.0 #test
        # batches = list()
        server_queue_batchs = list()
        wait_queue_batchs = list()
        system_queue_batchs = list()

        count = 0
        arrival_times = list()
        start_times = list()
        end_times = list()
        for line in trace:
            bt = list()
            
            attris = line.split()
            arv_t = float(attris[0])
            arrival_times.append(arv_t)
            stt_t = float(attris[2])
            start_times.append(stt_t)
            end_t = float(attris[3])
            end_times.append(end_t)
            count += 1

        arrival_times.sort()
        start_times.sort()
        end_times.sort()

        period_range = end_times[-1] - arrival_times[0]
        print('the whole period_range:', period_range)#test
        # print('util:', service_time / period_range)#test

        # Server queue length
        server_queue_length =\
            get_server_queue_length(start_times, end_times, period_range)
        RESULT.server_queue = server_queue_length
        # print('server_queue_length:', server_queue_length)

        # Wait queue length
        wait_queue_length = \
            get_wait_queue_length(arrival_times, start_times, period_range)
        RESULT.wait_queue = wait_queue_length
        # print('wait_queue_length:', wait_queue_length)

        # System queue length
        system_queue_length = \
            get_system_queue_length(arrival_times, end_times, period_range)
        RESULT.system_queue = system_queue_length
        # print('system_queue_length:', system_queue_length)

        # print('difference:')
        # print('wait + server:', wait_queue_length + server_queue_length)

def get_other_values(trace_file):
    '''Get average delay and average wait,
    also check with average service'''
    global RESULT
    global B
    global K
    with open(trace_file) as trace:
        count = 0
        # batches = list()
        delay_batches = list()
        wait_batches = list()
        delay_b = list()
        wait_b = list()
        delay_test = list()#test
        wait_test = list()#test
        service_times = list()
        for line in trace:
            attris = line.split()
            delay = float(attris[4])
            wait = float(attris[5])
            service = float(attris[1])
            delay_test.append(delay)#test
            wait_test.append(wait)#test
            delay_b.append(delay)
            wait_b.append(wait)
            service_times.append(service)
            if count % B == B - 1:
                delay_mean = stat.mean(delay_b)
                wait_mean = stat.mean(wait_b)
                delay_batches.append(delay_mean)
                wait_batches.append(wait_mean)
                delay_b.clear()
                wait_b.clear()
            count += 1
        alpha = 0.05
        k = K
        df = k - 1
        t_value = ss.t.ppf(1 - alpha/2, df)


        # State values of Delay
        delay_mean = stat.mean(delay_batches)
        delay_stdev = stat.pstdev(delay_batches)
        endpoint_delay = t_value * delay_stdev / (k - 1)**0.5

        # State values of Wait
        wait_mean = stat.mean(wait_batches)
        wait_stdev = stat.pstdev(wait_batches)
        endpoint_wait = t_value * wait_stdev / (k - 1)**0.5

        RESULT.wait = wait_mean
        RESULT.delay = delay_mean

        # print('delay_mean:', delay_mean)
        # print('test:', stat.mean(delay_test))
        print('endpoint_delay:', endpoint_delay)
        # print('wait_mean:', wait_mean)
        # print('test:', stat.mean(wait_test))
        print('endpoint_wait:', endpoint_wait)

        # Service time test
        service_mean = stat.mean(service_times)
        service_stdev = stat.pstdev(service_times)
        endpoint_service = t_value * service_stdev / (k - 1)**0.5
        print('endpoint_service:', endpoint_service)
        RESULT.service = service_mean
        # print('CHECK:')
        # print('service_mean:', service_mean)
        # print('service_mean + delay_mean:', service_mean + delay_mean)

        # Test
        # print("n:", B*K, 't:', )

def main():
    global RESULT
    directory = 'outputs/'
    # file_name = 'trace_sjf.csv'
    file_name = 'trace_fifo.csv'
    trace_file = directory + file_name
    # get_queue_lengths(trace_file)
    get_other_values(trace_file)
    print('Batches result:')
    get_queue_lengths_batches(trace_file)
    print(RESULT)
    print('==============================')
    print('Whole result:')
    get_queue_lengths_whole(trace_file)
    print(RESULT)

if __name__ == '__main__':
    main()