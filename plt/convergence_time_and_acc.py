import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys


Es = [1,5,20]
# colors = ['blue', 'green', 'orange']
log_dir = '../exp_1_remake/'
datasets = ['reddit', 'celeba', 'femnist']
targets = {
    'reddit': 0.095,
    'celeba' : 0.89,
    'femnist' : 0.8,
}


if __name__ == "__main__":
    cnt = 0
    small = 1
    big = 0
    small_acc = 1
    big_acc = 0
    
    for dataset in datasets:
        print(dataset)
        for E in Es:
            print(E)
            with open('{}/{}/{}_trace_{}.cfg.log'.format(log_dir,dataset,dataset,E), 'r') as f:
                t_convergence_time = 0
                t_final_acc = 0
                current_time = 0
                for line in f:
                    if 'current time:' in line:
                        floats = re.findall(r'\d+\.\d+',line)
                        current_time = float(floats[0])
                    if 'test_accuracy' in line:
                        floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                        t_final_acc = float(floats[0])
                        if t_final_acc > targets[dataset] and t_convergence_time==0:
                            t_convergence_time = current_time
                print('trace: convergence_time={}, final_acc={}'.format(t_convergence_time, t_final_acc))
            with open('{}/{}/{}_no_trace_{}.cfg.log'.format(log_dir,dataset,dataset,E), 'r') as f:
                nt_convergence_time = 0
                nt_final_acc = 0
                current_time = 0
                for line in f:
                    if 'current time:' in line:
                        floats = re.findall(r'\d+\.\d+',line)
                        current_time = float(floats[0])
                    if 'test_accuracy' in line:
                        floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                        nt_final_acc = float(floats[0])
                        if nt_final_acc > targets[dataset] and nt_convergence_time==0:
                            nt_convergence_time = current_time
                print('no trace: convergence_time={}, final_acc={}'.format(nt_convergence_time, nt_final_acc))
            tmp = t_convergence_time/nt_convergence_time - 1
            if tmp > 0:
                small = min(small, tmp)
                big = max(big, tmp)
            tmp = 1 - t_final_acc/nt_final_acc
            if tmp > 0:
                small_acc = min(small_acc, tmp)
                big_acc = max(big_acc, tmp)
    
    print('convergence time: {} ~ {}'.format(round(small,3), round(big,3)))
    print('final acc: {} ~ {}'.format(round(small_acc,3), round(big_acc,3)))