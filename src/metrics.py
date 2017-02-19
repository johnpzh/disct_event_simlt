'''Calculate mean, variance, standard deviation, and coefficient 
of variation (C.V.) of the inter-arrival times and service 
times.'''
from datetime import datetime
from datetime import timedelta
import numpy as np
import matplotlib.pyplot as plt

class Metrics:
    def __init__(self):
        self.iat_mean = 0
        self.iat_var = 0
        self.iat_sd = 0
        self.iat_cv = 0
        self.st_mean = 0
        self.st_var = 0
        self.st_sd = 0
        self.st_cv = 0

def get_metrics_all(trace_path, metrics):
    '''Get mean of all inter-arrival times and service times.'''
    with open(trace_path) as trace:
        # Mean
        count = 0
        interarrvl_times = list()
        service_times = list()
        # iat_sum = 0.0
        # st_sum = 0.0
        for line in trace:
            count += 1
            attrbts = line.split()
            interarrvl_time = float(attrbts[-2])
            service_time = float(attrbts[-1])
            if count != 1:
                interarrvl_times.append(interarrvl_time)
            service_times.append(service_time)
            # iat_sum += interarrvl_time
            # st_sum += service_time
        # iat_mean = iat_sum / (count - 1)
        # st_mean = st_sum / count
        iat_mean = sum(interarrvl_times) / (count - 1)
        st_mean = sum(service_times) / count
        metrics.iat_mean = iat_mean
        metrics.st_mean = st_mean

        # Variance
        iat_v = 0
        st_v = 0
        for i in range(count - 1):
            iat_v += (interarrvl_times[i] - iat_mean)**2
        for i in range(count):
            # iat_v += (interarrvl_times[i] - iat_mean)**2
            st_v += (service_times[i] - st_mean)**2
        iat_var = iat_v / (count - 1)
        st_var = st_v / count
        metrics.iat_var = iat_var
        metrics.st_var = st_var

        # Standard Deviation
        iat_sd = iat_var**0.5
        st_sd = st_var**0.5
        metrics.iat_sd = iat_sd
        metrics.st_sd = st_sd

        # Coefficient of Variation
        metrics.iat_cv = iat_sd / iat_mean
        metrics.st_cv = st_sd / st_mean

def get_metrics_time(trace_path):
    iat_file = 'inter-arrival-time_metrics.txt'
    with open(trace_path) as trace, \
        open(iat_file, 'w') as iat_output:
        
        one_day = timedelta(days=1)

        # Inter-arrival Time
        iat_mean_list = list()
        iat_var_list = list()
        iat_sd_list = list()
        iat_cv_list = list()
        iat_mean_q = 0
        iat_v_q = 0
        date_q = datetime(1996, 11, 1).day
        count = 0
        for line in trace:
            count += 1
            if count == 1:
                continue
            attrbts = line.split()
            arrival_t = float(attrbts[0])
            interarrvl_t = float(attrbts[-2])
            i = count - 1
            iat_mean = iat_mean_q + 1/i * (interarrvl_t - iat_mean_q)
            iat_v = iat_v_q + (i-1)/i * (interarrvl_t - iat_mean_q)**2
            date = datetime.fromtimestamp(arrival_t).day
            # print('@93 date:', date, 'timestamp', arrival_t)#test
            # print('@94 date:', datetime.fromtimestamp(arrival_t)) #tst
            if date > date_q:
                # print('date:', date, 'date_q', date_q)#test
                iat_mean_list.append(iat_mean)
                var = iat_v/i
                iat_var_list.append(var)
                sd = var**0.5
                iat_sd_list.append(sd)
                cv = sd / iat_mean
                iat_cv_list.append(cv)
            iat_mean_q = iat_mean
            iat_v_q = iat_v
            date_q = date

            if count % 100000 == 0:
                print('.', end='', flush=True)
        iat_mean_list.append(iat_mean)
        var = iat_v/i
        iat_var_list.append(var)
        sd = var**0.5
        iat_sd_list.append(sd)
        cv = sd / iat_mean
        iat_cv_list.append(cv)
        for i in range(len(iat_mean_list)):
            values = [str(i+1), \
                    str(iat_mean_list[i]), \
                    str(iat_var_list[i]), \
                    str(iat_sd_list[i]), \
                    str(iat_cv_list[i])]
            line = ' '.join(values) + '\n'
            iat_output.write(line)

        plt.figure(1)
        plt.xlabel('Number of Days')
        plt.ylabel('Mean of Inter-arrival Time')
        x = np.arange(1, len(iat_mean_list)+1, 1)
        y = iat_mean_list
        plt.plot(x, y)

        plt.show()
    
def test():
    # plt.figure(1)
    # x = np.arange(0, 21, 1)
    # y = 5.1 * np.ones((1, 21))
    x = [0, 20]
    y = [5.1, 5.1]
    plt.plot(x, y, 'b-')
    plt.show()
    print(x)
    print(y)

if __name__ == '__main__':
    # All trace
    # directory = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted/'
    # file_name = 'UCB-Trace-846890339-848409417.csv'

    # First part
    directory = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/extracted/'
    file_name = 'UCB-home-IP-846890339-847313219.csv'

    # Little sample
    # directory = '/scratch/zpeng.scratch/Dropbox/Works/homeworks/626 Data Analysis and Simulation/trace/sample/'
    # file_name = 'examples_times.csv'
    trace_path = directory + file_name
    
    # metrics = Metrics()
    # get_metrics_all(trace_path, metrics)
    # print('inter-arrival time mean:', metrics.iat_mean)
    # print('service time mean:', metrics.st_mean)
    # print('inter-arrival time var:', metrics.iat_var)
    # print('service time var:', metrics.st_var)
    # print('iat sd:', metrics.iat_sd)
    # print('st sd:', metrics.st_sd)
    # print('iat cv:', metrics.iat_cv)
    # print('st cv:', metrics.st_cv)

    get_metrics_time(trace_path)
    # test()