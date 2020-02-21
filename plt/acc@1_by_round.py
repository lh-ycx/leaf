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
log_dir = '../models/'
dataset = sys.argv[1]

if __name__ == "__main__":
    plt.figure()
    cnt = 0
    for E in Es:
        with open('{}{}_trace_{}.cfg.log'.format(log_dir,dataset,E), 'r') as f:
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
        plt.plot(x,y,color=colors[cnt],linewidth=0.75)
        cnt+=1
    cnt = 0
    for E in Es:
        with open('{}{}_no_trace_{}.cfg.log'.format(log_dir,dataset,E), 'r') as f:
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
        plt.plot(x,y,color=colors[cnt], ls='--')
        cnt+=1
    
    # plt.grid(axis='x',color='grey',ls='--')
    # x_major_locator=MultipleLocator(24)
    # ax=plt.gca()
    # ax为两条坐标轴的实例
    # ax.xaxis.set_major_locator(x_major_locator)
    
    font = {
            'weight' : 'normal',
            'size'   : 15,
            }
    plt.xlabel('round num', font)
    plt.ylabel('accuracy', font)
    plt.legend(["E = 1, with trace", 
                "E = 5, with trace", 
                "E = 20, with trace",
                "E = 1, without trace", 
                "E = 5, without trace", 
                "E = 20, without trace"])
    plt.savefig('{}_acc_by_round.png'.format(dataset))