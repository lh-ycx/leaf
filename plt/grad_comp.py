import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys

methods = ['nocomp', 'sign', 'structure_100', 'structure_1000', 'gdrop']
method2label = {
    'nocomp':'No Compression', 
    'sign': 'SignSGD',
    'structure_100': 'Structured Update, k=100', 
    'structure_1000': 'Structured Update, k=1000',
    'gdrop': 'GDrop'
}

Es = [1,5,20]
colors = ['red', 'green', 'brown', 'orange', 'blue']
log_dir = '../exp_3/'
dataset = 'grad_compress'
target_acc = 0.81

if __name__ == "__main__":
    plt.figure()
    fig,ax1 = plt.subplots(figsize=(6.5, 4))
    cnt = 0
    for method in methods:
        convergence_t = -1
        convergence_t_no_trace = -1
        final_acc_t = -1
        final_acc_no_t = -1
        with open('{}/{}/femnist_{}_trace_5.cfg.log'.format(log_dir,dataset,method), 'r') as f:
            x = []
            y = []
            
            current_time = 0
            current_round = 0
            hour = 0
            suc = 0

            for line in f:
                if 'Round' in line:
                    current_round = int(line.split()[9])
                if 'current time:' in line:
                    floats = re.findall(r'\d+\.\d+',line)
                    current_time = float(floats[0])
                if 'test_accuracy' in line:
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_acc = float(floats[0])
                    if convergence_t <= 0 and test_acc > target_acc:
                        convergence_t = current_time
                    if current_round > 500:
                        break
                    x.append(current_time/3600)
                    y.append(test_acc)
                    final_acc_t = test_acc
        x = np.array(x)
        y = np.array(y)
        if method == 'nocomp':
            lw = 2
        else:
            lw = 1.5
        plt.plot(x,y,color=colors[cnt], linewidth=lw, label = method2label[method], alpha=0.7)
        with open('{}/{}/femnist_{}_no_trace_5.cfg.log'.format(log_dir,dataset,method), 'r') as f:
            x = []
            y = []
            
            current_time = 0
            current_round = 0
            hour = 0
            suc = 0

            for line in f:
                if 'Round' in line:
                    current_round = int(line.split()[9])
                if 'current time:' in line:
                    floats = re.findall(r'\d+\.\d+',line)
                    current_time = float(floats[0])
                if 'test_accuracy' in line:
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_acc = float(floats[0])
                    if convergence_t_no_trace <= 0 and test_acc > target_acc:
                        convergence_t_no_trace = current_time
                    if current_round > 500:
                        break
                    x.append(current_time/3600)
                    y.append(test_acc)
                    final_acc_no_t = test_acc
        x = np.array(x)
        y = np.array(y)
        plt.plot(x,y,color=colors[cnt], ls=':',linewidth=1.5,)
        cnt+=1
        print('====={}====='.format(method))
        print('convergence_t: ', convergence_t)
        print('convergence_t_no_trace: ', convergence_t_no_trace)
        print('final_acc_t: ',final_acc_t)
        print('final_acc_no_t: ',final_acc_no_t)
        print('acc drop: ', 1-final_acc_t/final_acc_no_t)
        # print(convergence_t/convergence_t_no_trace - 1)
    
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
    # plt.title('', font_title)
    plt.xlabel('time line/h',font)
    plt.ylabel('accuracy',font)
    plt.legend(fontsize=12)
    fig.subplots_adjust(bottom=0.15)
    plt.savefig('grad_compression.png')