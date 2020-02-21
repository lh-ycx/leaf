import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log
import json

log_dir = '../models/'
colors = ['blue', 'green', 'orange']
Es = [1,5,20]

if __name__ == "__main__":
    plt.figure()    
    with open('{}clients_info_reddit_no_trace_5.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data_1 = np.array(data)
    with open('{}clients_info_reddit_trace_5.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data_2 = np.array(data)
    with open('{}clients_info_celeba_no_trace_1.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data_3 = np.array(data)
    with open('{}clients_info_celeba_trace_1.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data_4 = np.array(data)
    fig, ax = plt.subplots()
    ax.boxplot([data_1,data_2,data_3,data_4], notch=True, showfliers=False)
    font = {
        'weight' : 'normal',
        'size'   : 13,
        }
    ax.set_xticklabels(["reddit\n without trace", "reddit\n with trace", "celeba\n without trace", "celeba\n with trace"],font)
    # plt.hist(data, bins=100, normed=0, facecolor="blue", alpha=0.7)
    font = {
        'weight' : 'normal',
        'size'   : 17,
        }
    plt.title('Computation Distribution',font)
    # plt.xlabel('settings')
    # plt.ylabel('number of clients')
    
    plt.ylabel('relative computation',font)
    # fig.subplots_adjust(bottom=0.3)
    plt.savefig('computation_distribution.png')


           
