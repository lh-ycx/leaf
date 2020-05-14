import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys


Es = [1,5,20]
colors = ['blue', 'green', 'orange']
log_dir = '../exp_1_remake/'
dataset = sys.argv[1]
if dataset == 'femnist':
    target_acc = 0.81
elif dataset == 'reddit' or dataset == 'realworld_co':
    target_acc = 0.1
elif dataset == 'celeba':
    target_acc = 0.87

if __name__ == "__main__":
    plt.figure()
    fig,ax1 = plt.subplots(figsize=(6.5, 4))
    cnt = 0
    for E in Es:
        convergence_t = -1
        convergence_t_no_trace = -1
        if dataset == 'realworld_co':
            file = '{}/{}/{}_{}_trace.cfg.log'.format(log_dir,dataset,dataset,E)
        else:
            file = '{}/{}/{}_trace_{}.cfg.log'.format(log_dir,dataset,dataset,E)
        with open(file, 'r') as f:
            x = []
            y = []
            
            current_time = 0
            hour = 0
            suc = 0

            for line in f:
                if 'current time:' in line:
                    floats = re.findall(r'\d+\.\d+',line)
                    current_time = float(floats[0])
                if 'test_accuracy' in line:
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_acc = float(floats[0])
                    if convergence_t <= 0 and test_acc > target_acc:
                        convergence_t = current_time
                    x.append(current_time/3600)
                    y.append(test_acc)
        x = np.array(x)
        y = np.array(y)
        plt.plot(x,y,color=colors[cnt], lw=1.5,label='E={}, heterogeneity-aware'.format(E))
        cnt+=1
    cnt = 0
    for E in Es:
        if dataset == 'realworld_co':
            file = '{}/{}/{}_{}_no_trace.cfg.log'.format(log_dir,dataset,dataset,E)
        else:
            file = '{}/{}/{}_no_trace_{}.cfg.log'.format(log_dir,dataset,dataset,E)
        with open(file, 'r') as f:
            x = []
            y = []
            
            current_time = 0
            hour = 0
            suc = 0

            for line in f:
                if 'current time:' in line:
                    floats = re.findall(r'\d+\.\d+',line)
                    current_time = float(floats[0])
                if 'test_accuracy' in line:
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_acc = float(floats[0])
                    if convergence_t_no_trace <= 0 and test_acc > target_acc:
                        convergence_t_no_trace = current_time
                    x.append(current_time/3600)
                    y.append(test_acc)
        x = np.array(x)
        y = np.array(y)
        plt.plot(x,y,color=colors[cnt], ls=':', lw=1.5,label='E={}, heterogeneity-unaware'.format(E))
        cnt+=1
    
    
    '''print('====={} {}====='.format(dataset, E))
    print('convergence_t: ', convergence_t)
    print('convergence_t_no_trace: ', convergence_t_no_trace)
    print(convergence_t/convergence_t_no_trace - 1)'''
    
    plt.grid(axis='x',color='grey',ls='--')
    x_major_locator=MultipleLocator(12)
    ax=plt.gca()
    # ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    
    font = {
            'weight' : 'normal',
            'size'   : 24,
            }
    font_title = {
            'weight' : 'normal',
            'size'   : 28,
            }
    if dataset == 'realworld_co':
        plt.title('M-Type by time'.format(dataset), font_title)
    else:
        plt.title('{} by time'.format(dataset), font_title)
    plt.xlabel('time line/h',font)
    plt.ylabel('accuracy',font)
    plt.legend(fontsize=13)
    if dataset == 'realworld_co':
        plt.xlim([0,25])
    fig.subplots_adjust(bottom=0.15)
    plt.savefig('{}_acc_by_time.png'.format(dataset))