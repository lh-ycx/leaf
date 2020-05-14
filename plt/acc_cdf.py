import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log
import json
from collections import defaultdict
import matplotlib.patches as mpatches

log_dir = '../exp_1_remake/'
datasets = ['celeba', 'femnist', 'reddit', 'realworld_co']
colors = ['blue', 'green', 'orange']
Es = [1,5,20]

if __name__ == "__main__":
    for dataset in datasets:
        plt.figure()
        fig, ax = plt.subplots()
        cnt = 0
        for E in Es:
            if dataset == 'realworld_co':
                file_dir = '{}/{}/clients_info_{}_{}_no_trace.cfg.json'.format(log_dir,dataset,dataset,E)
            else:
                file_dir = '{}/{}/clients_info_{}_no_trace_{}.cfg.json'.format(log_dir,dataset,dataset,E)
            with open(file_dir, 'r') as f:
                client2acc = json.load(f)
                data = []
                for key in client2acc:
                    if dataset =='reddit' or dataset =='realworld_co':
                        data.append((client2acc[key]['acc'])[0])
                    else:
                        data.append((client2acc[key]['acc']))
                count = len(data)
                data.sort()
                x=[]
                y=[]
                for i in range(count):
                    x.append(data[i])
                    y.append((i+1)/count)
                median_no_trace = np.percentile(x,50)
                plt.plot(x,y,':',color=colors[cnt],label='E={}, Heterogeneity-unaware'.format(E))
            if dataset == 'realworld_co':
                file_dir = '{}/{}/clients_info_{}_{}_trace.cfg.json'.format(log_dir,dataset,dataset,E)
            else:
                file_dir = '{}/{}/clients_info_{}_trace_{}.cfg.json'.format(log_dir,dataset,dataset,E)
            with open(file_dir, 'r') as f:
                client2acc = json.load(f)
                data = []
                for key in client2acc:
                    if dataset =='reddit' or dataset =='realworld_co':
                        data.append((client2acc[key]['acc'])[0])
                    else:
                        data.append((client2acc[key]['acc']))
                count = len(data)
                data.sort()
                x=[]
                y=[]
                for i in range(count):
                    x.append(data[i])
                    y.append((i+1)/count)
                median_trace = np.percentile(x,50)
                plt.plot(x,y,'-',color=colors[cnt],label='E={}, Heterogeneity-aware'.format(E))
                cnt+=1
            print('{} {}: median_trace={}, median_no_trace={}, drop by {}'.format(dataset, E, median_trace, median_no_trace, 1-(median_trace/median_no_trace)))
        plt.xlabel('Accuracy', fontsize=20)
        plt.legend()
        if dataset == 'realworld_co':
            plt.title('M-Type', fontsize=25)
        else:
            plt.title(dataset, fontsize=25)    
        plt.ylabel('CDF', fontsize=20)
        # fig.subplots_adjust(bottom=0.3)
        if dataset == 'reddit' or dataset == 'realworld_co':
            plt.xlim([0,0.2])
        else:
            plt.xlim([0.2,1.1])
        fig.subplots_adjust(bottom=0.15)
        plt.savefig('acc_cdf_{}.png'.format(dataset))

           
