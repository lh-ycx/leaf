import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys

# paras = [25,50,100,200,500,1000]
colors = ['limegreen', 'orange', 'peru', 'red', 'darkred', 'black']
log_dir = '../exp_2/para/'
datasets = ['reddit', 'realworld']

if __name__ == "__main__":
    for dataset in datasets:
        if dataset == 'reddit':
            paras = [25,50,100,200,500,1000]
            target_acc = 0.11
            title = 'reddit'
        if dataset == 'realworld':
            paras = [25,50,100,200,300]
            target_acc = 0.1
            title = 'M-Type'
        plt.figure()
        cnt = 0
        for para in paras:
            with open('{}/para_{}_{}.cfg.log'.format(log_dir,dataset,para), 'r') as f:
                x = []
                y = []
                
                current_round = 0
                hour = 0
                suc = 0
                current_time = 0

                for line in f:
                    if 'Round' in line:
                        current_round = int(line.split()[9])
                    if 'current time' in line:
                        floats = re.findall(r'\d+\.\d+',line)
                        current_time = float(floats[0])
                    if 'test_accuracy' in line:
                        floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                        test_acc = float(floats[0])
                        if test_acc > 1:
                            print(floats)
                            assert False
                        x.append(current_time/3600)
                        y.append(test_acc)
            x = np.array(x)
            y = np.array(y)
            plt.plot(x,y,color=colors[cnt],linewidth=0.75, label = 'para = {}'.format(para))
            cnt+=1
        plt.grid(axis='x',color='grey',ls='--')
        x_major_locator=MultipleLocator(12)
        ax=plt.gca()
        # ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        font = {
                'weight' : 'normal',
                'size'   : 20,
                }
        plt.xlabel('Time Line (hour)', font)
        plt.ylabel('Accuracy', font)
        plt.legend()
        plt.savefig('para_acc_{}.png'.format(dataset))

        
        plt.figure()
        fig,ax1 = plt.subplots()
        ax1.set_xlabel('Parallel Degree',fontsize=20)
        ax1.set_ylabel('Accuracy',fontsize=19)
        ax2 = ax1.twinx()
        ax2.set_ylabel('Convergence Time (sec)',fontsize=19)
        # x = np.array(list(map(log, ddls)))
        x = np.array(paras)
        y = []
        x2 = []
        y2 = []
        y_min = 9999999.0
        y_max = 0.0
        for para in paras:
            current_time = 0
            with open('{}/para_{}_{}.cfg.log'.format(log_dir,dataset,para), 'r') as f:
                convergence_flag = False
                max_acc = 0
                for line in f:
                    if 'current time' in line:
                        floats = re.findall(r'\d+\.\d+',line)
                        current_time = float(floats[0])
                    if 'test_accuracy' in line:
                        floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                        test_acc = float(floats[0])
                        max_acc = max(max_acc, test_acc)
                        # if dataset == 'reddit':
                        #     test_acc = float(floats[5])
                        if test_acc > target_acc and not convergence_flag:
                            x2.append(para)
                            y2.append(current_time)
                            convergence_flag = True
                            y_max = max(current_time,y_max)
                            y_min = min(current_time,y_min)   
                y.append(max_acc)
                if convergence_flag == False:
                    x2.append(para)
                    y2.append(200000)
        y = np.array(y)
        print('x:{}'.format(x))
        print('y:{}'.format(y))
        l_1 = ax1.plot(x,y,'o-',color='red',label='Accuracy')
        l_2 = ax2.plot(x2,y2,'X-',color='blue', label='Convergence Time (sec)')
        ax2.axis([None,None,y_min*0.99,y_max*1.01])
        if dataset == 'reddit' or dataset == 'realworld':
            ax1.axis([None,None,0.05,max(y) *1.02])
        ls = l_1 + l_2
        labels = [l.get_label() for l in ls]
        ax1.legend(ls, labels,fontsize=18)
        fig.subplots_adjust(right=0.85)
        plt.title(title,fontsize=25)
        plt.savefig('para_{}_to_reach_{}.png'.format(dataset,target_acc))


        '''
        plt.figure()
        cnt = 0
        x = paras
        y = []
        for para in paras:
            flag = True
            current_time = 0
            with open('{}/para_{}_{}.cfg.log'.format(log_dir,dataset,para), 'r') as f:
                for line in f:
                    if 'Round' in line:
                        current_round = int(line.split()[9])
                    if 'current time' in line:
                        floats = re.findall(r'\d+\.\d+',line)
                        current_time = float(floats[0])
                    if 'test_accuracy' in line:
                        floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                        test_acc = float(floats[0])
                        if test_acc > target_acc:
                            y.append(current_time)
                            flag = False
                            break
                if flag:
                    y.append(current_time)
        y = np.array(y)
        plt.plot(x,y,'X-',color='blue', label='convergence time')

        font = {
                'weight' : 'normal',
                'size'   : 20,
                }
        plt.xlabel('client num per round', font)
        plt.ylabel('convergence time (sec)', font)
        plt.legend()
        plt.savefig('para_round_to_reach_{}.png'.format(target_acc))
        '''