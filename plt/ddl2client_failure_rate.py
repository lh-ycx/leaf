import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log
import re

datasets = ['celeba', 'femnist']

if __name__ == "__main__":
    for dataset in datasets:
        if dataset == 'femnist':
            ddls = [210,230,250,270,290,310,330,350]
            log_dir = '../exp_2_remake/femnist_ddl/'
            target_acc = 0.81
        if dataset == 'celeba':
            ddls = [60,70,80,90,100,120,150]
            log_dir = '../exp_2_remake/celeba_ddl/'
            target_acc = 0.88
        plt.figure()
        fig,ax1 = plt.subplots()
        ax1.set_xlabel('Deadline (sec)',fontsize=20)
        ax1.set_ylabel('Client Failure Rate',fontsize=19)
        ax2 = ax1.twinx()
        ax2.set_ylabel('Convergence Time (sec)',fontsize=19)
        # x = np.array(list(map(log, ddls)))
        x = np.array(ddls)
        y = []
        x2 = []
        y2 = []
        y_min = 9999999.0
        y_max = 0.0
        for ddl in ddls:
            if dataset == 'femnist':
                log_file = '{}{}_ddl_5_{}.cfg.log'.format(log_dir,dataset, ddl)
            else:
                log_file = '{}{}_ddl_{}.cfg.log'.format(log_dir,dataset, ddl)
            with open(log_file, 'r') as f:
                suc = 0
                fail = 0
                convergence_flag = False
                upload_fractions = []
                for line in f:
                    if 'round succeed' in line:
                        suc+=1
                    if 'round failed' in line:
                        fail+=1
                    if 'current time' in line:
                        floats = re.findall(r'\d+\.\d+',line)
                        current_time = float(floats[0])
                    if 'clients upload' in line:
                        upload_cnt = int(line.split()[7])
                        total_cnt = int(line.split()[9])
                        upload_fractions.append(upload_cnt/total_cnt)
                    if 'test_accuracy' in line:
                        floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                        test_acc = float(floats[0])
                        if dataset == 'reddit':
                            test_acc = float(floats[5])
                        if test_acc > target_acc:
                            print(ddl, current_time)
                            x2.append(ddl)
                            y2.append(current_time)
                            convergence_flag = True
                            y_max = max(current_time,y_max)
                            y_min = min(current_time,y_min)
                            break
                average_upload_fraction = sum(upload_fractions)/len(upload_fractions)
                y.append(1-average_upload_fraction)
                if convergence_flag == False:
                    x2.append(ddl)
                    y2.append(200000)
        y = np.array(y)
        print('x:{}'.format(x))
        print('y:{}'.format(y))
        l_1 = ax1.plot(x,y,'o-',color='brown',label='Client Failure Rate')
        l_2 = ax2.plot(x2,y2,'X-',color='blue', label='Convergence Time')
        l_3 = ax1.axhline(y=0.125,ls=":",c="red",label='Minimum Reporting Fraction')#添加水平直线
        l_3 = ax1.axhline(y=0.075,ls=":",c="red",label='Minimum Reporting Fraction')#添加水平直线
        ax2.axis([None,None,y_min*0.99,y_max*1.01])
        ls = l_1 + l_2
        labels = [l.get_label() for l in ls]
        ax1.legend(ls, labels,fontsize=18)
        fig.subplots_adjust(right=0.85,left=0.15)
        plt.title(dataset,fontsize=25)
        plt.savefig('ddl2client_failure_rate_{}.png'.format(dataset))