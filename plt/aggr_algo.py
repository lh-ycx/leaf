import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys

methods = ['fedavg', 'qffl', 'fedprox']
method2label = {
    'nocomp':'No Compression', 
    'sign': 'SignSGD',
    'structure_100': 'Structured Update, k=100', 
    'structure_1000': 'Structured Update, k=1000',
    'gdrop': 'GDrop'
}

datasets = ['reddit', 'femnist']
colors = ['red', 'green', 'blue', 'orange', 'blue']
log_dir = '../exp_3/aggre_algo/aggr/'
# dataset = 'grad_compress'


if __name__ == "__main__":
    for dataset in datasets:
        if dataset == 'femnist':
            target_acc = 0.81
        if dataset == 'reddit' :
            target_acc = 0.1
        plt.figure()
        fig,ax1 = plt.subplots(figsize=(6.5, 4))
        cnt = 0
        for method in methods:
            convergence_t = -1
            convergence_t_no_trace = -1
            final_acc_t = -1
            final_acc_no_t = -1
            with open('{}/aggr_{}_{}_trace.cfg.log'.format(log_dir,method,dataset), 'r') as f:
                x = []
                y = []
                
                current_time = 0
                current_round = 0
                hour = 0
                suc = 0

                for line in f:
                    if 'Round' in line:
                        current_round = int(line.split()[9])
                        if current_round > 300:
                            break
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
                        x.append(current_round)
                        y.append(test_acc)
                        final_acc_t = test_acc
            x = np.array(x)
            y = np.array(y)
            if method == 'nocomp':
                lw = 2
            else:
                lw = 1.5
            plt.plot(x,y,color=colors[cnt], linewidth=lw,alpha=0.7,label = '{}, hete-aware'.format(method))
            with open('{}/aggr_{}_{}_no_trace.cfg.log'.format(log_dir,method,dataset), 'r') as f:
                x = []
                y = []
                
                current_time = 0
                current_round = 0
                hour = 0
                suc = 0

                for line in f:
                    if 'Round' in line:
                        current_round = int(line.split()[9])
                        if current_round > 300:
                            break
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
                        x.append(current_round)
                        y.append(test_acc)
                        final_acc_no_t = test_acc
            x = np.array(x)
            y = np.array(y)
            plt.plot(x,y,color=colors[cnt], ls=':',linewidth=1.5,label='{}, hete-unaware'.format(method))
            cnt+=1
            print('====={}====='.format(method))
            print('convergence_t: ', convergence_t)
            print('convergence_t_no_trace: ', convergence_t_no_trace)
            print('final_acc_t: ',final_acc_t)
            print('final_acc_no_t: ',final_acc_no_t)
            print('acc drop: ', 1-final_acc_t/final_acc_no_t)
            # print(convergence_t/convergence_t_no_trace - 1)
        
        plt.title(dataset, fontsize=25)

        '''
        plt.grid(axis='x',color='grey',ls='--')
        x_major_locator=MultipleLocator(6)
        ax=plt.gca()
        # ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        '''
        
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
        if dataset == 'femnist':
            plt.ylim([0.55, 0.9])
        fig.subplots_adjust(bottom=0.15)
        plt.savefig('aggr_{}.png'.format(dataset))