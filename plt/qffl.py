import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys
import json

methods = ['fedavg', 'qffl']

datasets = ['realworld_co', 'femnist']
colors = ['red', 'blue', 'green', 'orange', 'blue']
log_dir = '../exp_3/aggre_algo/aggr/'
# dataset = 'grad_compress'


if __name__ == "__main__":
    for dataset in datasets:
        if dataset == 'femnist':
            target_acc = 0.81
        if dataset == 'reddit' :
            target_acc = 0.1
        if dataset == 'realworld_co':
            target_acc = 0.9
        
        for method in methods:
            file = '{}/clients_info_aggr_{}_{}_trace.cfg.json'.format(log_dir,method,dataset)
            if dataset == 'femnist' and method == 'qffl':
                file = '{}/clients_info_aggr_{}_{}_trace_0.001.cfg.json'.format(log_dir,method,dataset)
            print('{} {} hete-aware:'.format(dataset,method))
            with open(file, 'r') as f:
                data = json.load(f)
                accs = []
                for key in data.keys():
                    if dataset == 'realworld_co':
                        accs.append(data[key]['acc'][3])
                    if dataset == 'femnist':
                        accs.append(data[key]['acc'])
                w_10 = np.percentile(accs,10)
                b_10 = np.percentile(accs,90)
                mean = np.mean(accs)
                var = np.var(accs)
                print('average ({}), worst 10% ({}), best 10% ({}), var ({})'.format(mean,w_10,b_10,var))
            
            file = '{}/clients_info_aggr_{}_{}_no_trace.cfg.json'.format(log_dir,method,dataset)
            if dataset == 'femnist' and method == 'qffl':
                file = '{}/clients_info_aggr_{}_{}_no_trace_0.001.cfg.json'.format(log_dir,method,dataset)
            print('{} {} hete-unaware:'.format(dataset,method))
            with open(file, 'r') as f:
                data = json.load(f)
                accs = []
                for key in data.keys():
                    if dataset == 'realworld_co':
                        accs.append(data[key]['acc'][3])
                    if dataset == 'femnist':
                        accs.append(data[key]['acc'])
                w_10 = np.percentile(accs,10)
                b_10 = np.percentile(accs,90)
                mean = np.mean(accs)
                var = np.var(accs)
                print('average ({}), worst 10% ({}), best 10% ({}), var ({})'.format(mean,w_10,b_10,var))

