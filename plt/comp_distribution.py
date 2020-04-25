import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log
import json

log_dir = '../exp_1_remake/'
colors = ['blue', 'green', 'orange']
Es = [1,5,20]

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(1,1))    
    # plt.figure(dpi=500, figsize=(20, 6))
    with open('{}/reddit/clients_info_reddit_no_trace_5.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data_1 = np.array(data)
    with open('{}/reddit/clients_info_reddit_trace_5.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data_2 = np.array(data)
        median = np.percentile(data_2, 50)
        acc = []
        inactive_acc = []
        for key in client2comp:
            acc.append(float(client2comp[key]['acc'][0]))
            comp = int(client2comp[key]['comp'])/10
            if comp <= median:
                inactive_acc.append(float(client2comp[key]['acc'][0]))
        print('reddit clients\' acc: {}'.format(np.mean(acc)))
        print('reddit in-active clients\' acc: {}'.format(np.mean(inactive_acc)))
        print(1-np.mean(inactive_acc)/np.mean(acc))
    with open('{}/celeba/clients_info_celeba_no_trace_1.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data_3 = np.array(data)
    with open('{}/celeba/clients_info_celeba_trace_1.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data_4 = np.array(data)
        median = np.percentile(data_4, 50)
        acc = []
        inactive_acc = []
        for key in client2comp:
            acc.append(float(client2comp[key]['acc']))
            comp = int(client2comp[key]['comp'])/10
            if comp <= median:
                inactive_acc.append(float(client2comp[key]['acc']))
        print('celeba clients\' acc: {}'.format(np.mean(acc)))
        print('celeba in-active clients\' acc: {}'.format(np.mean(inactive_acc)))
        print(1-np.mean(inactive_acc)/np.mean(acc))
    with open('{}/femnist/clients_info_femnist_no_trace_1.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/1000)
        data_5 = np.array(data)
    with open('{}/femnist/clients_info_femnist_trace_1.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/1000)
        data_6 = np.array(data)
        median = np.percentile(data_6, 50)
        acc = []
        inactive_acc = []
        for key in client2comp:
            acc.append(float(client2comp[key]['acc']))
            comp = int(client2comp[key]['comp'])/10
            if comp <= median:
                inactive_acc.append(float(client2comp[key]['acc']))
        print('femnist clients\' acc: {}'.format(np.mean(acc)))
        print('femnist in-active clients\' acc: {}'.format(np.mean(inactive_acc)))
        print(1-np.mean(inactive_acc)/np.mean(acc))
    fig, ax = plt.subplots()
    ax.boxplot([data_1,data_2,data_3,data_4,data_5,data_6], notch=True, showfliers=False)
    font = {
        'weight' : 'normal',
        'size'   : 15,
        }
    ax.set_xticklabels(["reddit\n ideal", 
                        "reddit\n olaf", 
                        "celeba\n ideal", 
                        "celeba\n olaf",
                        "femnist\n ideal",
                        "femnist\n olaf"],font)
    # plt.hist(data, bins=100, normed=0, facecolor="blue", alpha=0.7)
    font = {
        'weight' : 'normal',
        'size'   : 16,
        }
    plt.title('Computation Distribution',font)
    # plt.xlabel('settings')
    # plt.ylabel('number of clients')
    
    plt.ylabel('relative computation',font)
    fig.subplots_adjust(bottom=0.15)
    plt.savefig('computation_distribution.png')


           
