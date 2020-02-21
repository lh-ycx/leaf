import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log
import json
from collections import defaultdict
import matplotlib.patches as mpatches

log_dir = '../models/'
colors = ['blue', 'green', 'orange']
Es = [1,5,20]

if __name__ == "__main__":
    plt.figure()    
    with open('{}clients_info_reddit_no_trace_5.cfg.json'.format(log_dir), 'r') as f:
        client2acc = json.load(f)
        data = []
        for key in client2acc:
            data.append((client2acc[key]['acc'])[0])
        data_1 = np.array(data)
    with open('{}clients_info_reddit_trace_5.cfg.json'.format(log_dir), 'r') as f:
        client2acc = json.load(f)
        data = []
        for key in client2acc:
            data.append((client2acc[key]['acc'])[0])
        data_2 = np.array(data)
    with open('{}clients_info_celeba_no_trace_5.cfg.json'.format(log_dir), 'r') as f:
        client2acc = json.load(f)
        data_3 = defaultdict(int)
        for key in client2acc:
            data_3[str(client2acc[key]['acc'])] += 1
    with open('{}clients_info_celeba_trace_5.cfg.json'.format(log_dir), 'r') as f:
        client2acc = json.load(f)
        data_4 = defaultdict(int)
        for key in client2acc:
            data_4[str(client2acc[key]['acc'])] += 1
    fig, ax = plt.subplots()
    ax.boxplot([data_1,data_2], notch=True, showfliers=False)
    font = {
        'weight' : 'normal',
        'size'   : 13,
        }
    ax.set_xticklabels(["reddit\n without trace", "reddit\n with trace"],font)
    # plt.hist(data, bins=100, normed=0, facecolor="blue", alpha=0.7)
    font = {
        'weight' : 'normal',
        'size'   : 17,
        }
    plt.title('Reddit Acc Distribution',font)    
    plt.ylabel('acc',font)
    # fig.subplots_adjust(bottom=0.3)
    plt.savefig('reddit_acc_distribution.png')

    plt.figure()
    for key in data_3:
        x = float(key)
        y = data_3[key]
        plt.bar(x,y,width=0.05,label=key,color='b')
    
    for key in data_4:
        x = float(key) + 0.05
        y = data_4[key]
        plt.bar(x,y,width=0.05,label=key,color='r')
    
    plt.xlabel('Accuracy', font)
    color = ['blue', 'red']
    labels = ['no trace', 'trace']
    patches = [ mpatches.Patch(color=color[i], label="{}".format(labels[i]) ) for i in range(len(color)) ] 
    plt.legend(handles=patches, ncol=2)
    plt.title('Celeba Acc Distribution',font)    
    plt.ylabel('Client Num',font)
    # fig.subplots_adjust(bottom=0.3)
    plt.savefig('celeba_acc_distribution.png')

           
