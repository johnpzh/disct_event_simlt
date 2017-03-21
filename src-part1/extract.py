import os
import subprocess as sp
from datetime import datetime
from datetime import timedelta

def get_time(attris, index):
    """From list attris[index], return timestamp and microsecond"""
    timestamp, microsec = attris[index].split(':')
    timestamp = float(timestamp)
    microsec = float(microsec)
    return timestamp, microsec

def extract_to_file(trace_path, extracted):
    """ From traces, extract inter-arrival times and service times."""
    # from_dirct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/'
    # file_name = 'UCB-home-IP-846890339-847313219.csv'
    # # file_name = 'examples.csv'
    # trace_path = from_dirct + file_name
    # to_dirct = '../extracted/'
    # extracted = to_dirct + file_name
    with open(trace_path, encoding='iso8859_15') as trace:
    # Make a New Trace by sorting the old trace 
    # according to Arrival Time
        print('For file:', trace_path, flush=True)
        trace_new = list()
        count = 0
        for line in trace:
            attris = line.split()

            # Arrival Time
            timestamp, microsec = get_time(attris, 0)
            arrival_time = datetime.fromtimestamp(timestamp)
            arrival_time = arrival_time \
                        + timedelta(microseconds=microsec)
            arrival_time = arrival_time.timestamp()

            # Start Time
            timestamp, microsec = get_time(attris, 1)
            start_time = datetime.fromtimestamp(timestamp)
            start_time = start_time \
                        + timedelta(microseconds=microsec)
            start_time = start_time.timestamp()

            # End Time
            timestamp, microsec = get_time(attris, 2)
            end_time = datetime.fromtimestamp(timestamp)
            end_time = end_time \
                        + timedelta(microseconds=microsec)
            end_time = end_time.timestamp()

            # Response Data Length
            length = attris[11]
            length = int(length)

            if length == 0:
            # Skip those abnormal records
                continue

            result = [arrival_time, start_time, end_time, length]
            trace_new.append(result)
            count += 1
            if count % 10000 == 0:
                print('.', end='', flush=True) 
        # Sort
        trace_new.sort(key=lambda record: record[0])
        # print(trace_new)

    # with open(trace_path) as trace, \
    #     open(extracted, 'w') as output:
    print('\nWriting', flush=True)
    with open(extracted, 'w') as output:
        is_first = True
        count = 0
        for line in trace_new:
            # Arrival Time
            arrival_time_ts = line[0]
            arrival_time = datetime.fromtimestamp(arrival_time_ts)

            # Start Time
            start_time_ts = line[1]
            start_time = datetime.fromtimestamp(start_time_ts)

            # End Time
            end_time_ts = line[2]
            end_time = datetime.fromtimestamp(end_time_ts)

            # Response Data Length
            length = line[3]

            if is_first:
                at_last = arrival_time
                is_first = False

            # Get Inter-arrival Time
            inter_arrival = arrival_time - at_last
            inter_arrival = inter_arrival / timedelta(seconds=1)

            # Get Service Time
            service_time = end_time - start_time
            service_time = service_time / timedelta(seconds=1)

            # Save Last Arrival Time
            at_last = arrival_time

            # Write Record to new file
            result = [str(arrival_time_ts), \
                        str(start_time_ts), \
                        str(end_time_ts), \
                        str(length), \
                        str(inter_arrival), \
                        str(service_time)]
            result = ' '.join(result) + '\n'
            output.write(result)
            count += 1
            if count % 10000 == 0:
                print('.', end='', flush=True) 
    print("\nOne is done.", flush=True)

def extract():
    from_dirct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/'
    # from_dirct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/sample/'
    entries = os.listdir(from_dirct)
    for entry in entries:
        if entry[-4:] != '.csv':
            continue
        file_name = entry
        trace_path = from_dirct + file_name
        to_dirct = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted/'
        extracted = to_dirct + file_name
        extract_to_file(trace_path, extracted)

    # file_name = 'UCB-home-IP-846890339-847313219.csv'
    # file_name = 'examples.csv'
    # trace_path = from_dirct + file_name
    # to_dirct = '../extracted/'
    # extracted = to_dirct + file_name

def test():
    # time = datetime(second=846890339, microsecond=661920)
    time = datetime.fromtimestamp(846890339)
    dt = timedelta(microseconds=661920)
    time = time + dt

    t2 = datetime.fromtimestamp(846890339)
    dt = timedelta(microseconds=989181)
    t2 = t2 + dt
    # time.microsecond = 661920
    inter_arrival = t2 - time
    microsec = inter_arrival / timedelta(microseconds=1)
    print('Time:', time)
    print('Inter-arrival time:', inter_arrival, microsec)
    print('Timestamp:', time.timestamp())

if __name__ == '__main__':
    extract()
    # test()
