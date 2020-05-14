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

if __name__ == "__main__":
    plt.figure()
    fig,ax1 = plt.subplots(figsize=(6.5, 4))
    cnt = 0
    real_acc = [0.0] * 3
    ideal_acc = [0.0] * 3
    for E in Es:
        if dataset == 'realworld_co':
            file = '{}/{}/{}_{}_trace.cfg.log'.format(log_dir,dataset,dataset,E)
        else:
            file = '{}/{}/{}_trace_{}.cfg.log'.format(log_dir,dataset,dataset,E)
        with open(file, 'r') as f:
            x = []
            y = []
            
            current_round = 0
            hour = 0
            suc = 0

            for line in f:
                if 'Round' in line:
                    current_round = int(line.split()[9])
                if 'test_accuracy' in line:
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_acc = float(floats[0])
                    if test_acc > 1:
                        print(floats)
                        assert False
                    x.append(current_round)
                    y.append(test_acc)
        x = np.array(x)
        y = np.array(y)
        plt.plot(x,y,color=colors[cnt],lw=1.5,label='E={}, heterogeneity-aware'.format(E))
        real_acc[cnt] = test_acc
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
            
            current_round = 0
            hour = 0
            suc = 0

            for line in f:
                if 'Round' in line:
                    current_round = int(line.split()[9])
                if 'test_accuracy' in line:
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_acc = float(floats[0])
                    if test_acc > 1:
                        print('E: {}, round: {}'.format(E,current_round))
                        print(floats)
                        break
                    x.append(current_round)
                    y.append(test_acc)
        x = np.array(x)
        y = np.array(y)
        plt.plot(x,y,color=colors[cnt], ls='--',lw=1.5, label='E={}, heterogeneity-unaware'.format(E))
        ideal_acc[cnt] = test_acc
        cnt+=1

    for i in range(3):
        print('acc drops by:', (ideal_acc[i] - real_acc[i]) / ideal_acc[i])


    # plt.grid(axis='x',color='grey',ls='--')
    # x_major_locator=MultipleLocator(24)
    # ax=plt.gca()
    # ax为两条坐标轴的实例
    # ax.xaxis.set_major_locator(x_major_locator)
    
    font = {
            'weight' : 'normal',
            'size'   : 24,
            }
    font_title = {
            'weight' : 'normal',
            'size'   : 28,
            }
    if dataset == 'realworld_co':
        plt.title('M-Type by round'.format(dataset), font_title)
    else:
        plt.title('{} by round'.format(dataset), font_title)
    plt.xlabel('round num', font)
    plt.ylabel('accuracy', font)
    plt.legend(fontsize=13)
    fig.subplots_adjust(bottom=0.15)
    plt.savefig('{}_acc_by_round.png'.format(dataset))