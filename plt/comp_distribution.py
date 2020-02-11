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
    with open('{}client2cnt.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key])/10)
        data = np.array(data)
    fig, ax = plt.subplots()
    ax.boxplot([data,data, data, data], notch=True, showfliers=False)
    ax.set_xticklabels(["reddit\n without trace", "reddit\n with trace", "celeba\n without trace", "celeba\n with trace"])
    # plt.hist(data, bins=100, normed=0, facecolor="blue", alpha=0.7)
    plt.title('Computation Distribution')
    # plt.xlabel('settings')
    # plt.ylabel('number of clients')
    plt.ylabel('relative computation')
    # fig.subplots_adjust(bottom=0.3)
    plt.savefig('computation_distribution.png')


           
