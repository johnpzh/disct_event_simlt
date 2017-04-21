'''Get the record of waiting queue length, 
then get its distribution by the form of 
histogram.'''
import os
import subprocess as sp
import numpy as np
import heapq as hq
import statistics as stat
import scipy.stats as ss
from datetime import datetime
from datetime import timedelta

