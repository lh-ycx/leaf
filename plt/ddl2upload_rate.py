import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log
import re

ddls = [40,50,60,70,80,90]
log_dir = '../exp_2/reddit/'

if __name__ == "__main__":
    plt.figure()
    fig,ax1 = plt.subplots()
    ax1.set_xlabel('ddl/s')
    ax1.set_ylabel('Round Fail Rate')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Average Upload Fraction')
    # x = np.array(list(map(log, ddls)))
    x = np.array(ddls)
    y = []
    x2 = np.array(ddls)
    y2 = []
    for ddl in ddls:
        with open('{}reddit_ddl_{}.cfg.log'.format(log_dir, ddl), 'r') as f:
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
    l_1 = ax1.plot(x,y,'o-',color='blue',label='Round Fail rate')
    l_2 = ax2.plot(x2,y2,'X-',color='red', label='Average Upload Fraction')
    # ax2.axis([None,None,y_min*0.99,y_max*1.01])
    ls = l_1 + l_2
    labels = [l.get_label() for l in ls]
    ax1.legend(ls, labels)
    fig.subplots_adjust(right=0.85)
    plt.axhline(y=0.8,ls=":",c="red")#添加水平直线
    plt.savefig('ddl2upload_rate.png')