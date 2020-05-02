import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log
import re

datasets = ['reddit', 'femnist']

if __name__ == "__main__":
    for dataset in datasets:
        if dataset == 'femnist':
            ddls = [210,230,250,270,290,310,330,350]
            log_dir = '../exp_2_remake/femnist_ddl/'
            target_acc = 0.81
        else:
            ddls = [40,50,60,70,80,90]
            log_dir = '../exp_2/reddit/'
            target_acc = 0.1
        
        plt.figure()
        fig,ax1 = plt.subplots()
        ax1.set_xlabel('ddl/s',fontsize=20)
        ax1.set_ylabel('Round Failure Rate',fontsize=20)
        ax2 = ax1.twinx()
        ax2.set_ylabel('Average Reporting Fraction',fontsize=20)
        # x = np.array(list(map(log, ddls)))
        x = np.array(ddls)
        y = []
        x2 = np.array(ddls)
        y2 = []
        for ddl in ddls:
            if dataset == 'femnist':
                log_file = '{}{}_ddl_5_{}.cfg.log'.format(log_dir,dataset, ddl)
            else:
                log_file = '{}{}_ddl_{}.cfg.log'.format(log_dir,dataset, ddl)
            with open(log_file, 'r') as f:
                suc = 0
                fail = 0
                upload_fractions = []
                for line in f:
                    if 'round succeed' in line:
                        suc+=1
                    if 'round failed' in line:
                        fail+=1
                    if 'clients upload' in line:
                        upload_cnt = int(line.split()[7])
                        total_cnt = int(line.split()[9])
                        upload_fractions.append(upload_cnt/total_cnt)
                y.append(fail/(fail+suc))
                average_upload_fraction = sum(upload_fractions)/len(upload_fractions)
                y2.append(average_upload_fraction)
        y = np.array(y)
        print('x:{}'.format(x))
        print('y:{}'.format(y))
        l_1 = ax1.plot(x,y,'o-',color='blue',label='Round Failure Rate')
        l_2 = ax2.plot(x2,y2,'X-',color='red', label='Average Reporting Fraction')
        l_3 = plt.axhline(y=0.8,ls=":",c="red",label='Minimum Reporting Fraction')#添加水平直线
        # ax2.axis([None,None,y_min*0.99,y_max*1.01])
        ls = l_1 + l_2 + [l_3]
        labels = [l.get_label() for l in ls]
        ax1.legend(ls, labels,fontsize=12)
        fig.subplots_adjust(right=0.85)
        plt.title(dataset,fontsize=25)
        plt.savefig('ddl2upload_rate_{}.png'.format(dataset))