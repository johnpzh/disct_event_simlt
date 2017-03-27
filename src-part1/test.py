import os
import subprocess as sp
import numpy as np
from datetime import datetime
from datetime import timedelta

def test2():
    with open('test.py') as input:
        count = 0
        for line in input:
            count += 1
            print(count, line)

def test():
    for i in range(1, 2):
        print(i)
    pack_list = []
    pack_list.append([])
    a = [1]
    pack_list.extend(a)
    print(pack_list)

    a = [[1, 'b'], [0, 'a']]
    a.sort(key=lambda x:x[0])
    print(a)

    with open('test.py') as input:
        count = 0
        for line in input:
            count += 1
            print(count, line)
            test2()

def test3():
    a = [[0], [1], [2]]

    for attris in a:
        attris.append('a')
    print(a)

def test4():
    factor_min = 0.102632009
    factor_max =  0.923688084
    a = np.linspace(factor_min, factor_max, 10)
    print(a)

    a = 1
    print('{0:04d}'.format(a))

    a = np.arange(1, 10, 2)
    print(a)

if __name__ == '__main__':
    test4()