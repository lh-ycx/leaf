import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log
import re

ddls = [70,170,270,520,1020,2020,4020]
log_dir = '../exp_2/interrupt/'

if __name__ == "__main__":
    plt.figure()
    fig,ax1 = plt.subplots()
    ax1.set_xlabel('ddl/s')
    ax1.set_ylabel('Average Interruption Rate')
    # ax2 = ax1.twinx()
    # ax2.set_ylabel('Convergence Time/s')
    # x = np.array(list(map(log, ddls)))
    x = np.array(ddls)
    y = []
    for ddl in ddls:
        with open('{}femnist_interrupt_{}.cfg.log'.format(log_dir, ddl), 'r') as f:
            total = 100
            interrupt = 0
            interrupts = []
            round_num = 0
            for line in f:
                if 'Round' in line:
                    if round_num > 0:
                        interrupts.append(interrupt/total)
                    round_num += 1
                    interrupt = 0
                if 'client interruption' in line:
                    interrupt+=1
            interrupts.append(interrupt/total)
            y.append(sum(interrupts)/len(interrupts))
    y = np.array(y)
    print('x:{}'.format(x))
    print('y:{}'.format(y))
    l_1 = ax1.plot(x,y,'o-',color='blue',label='Average Interruption Rate')
    l_2 = ax1.axvline(x=2375.78,ls=":",c="red", label='Average Available Interval Length') #添加垂直直线
    # l_2 = ax2.plot(x2,y2,'X-',color='red', label='Convergence Time')
    # ax2.axis([None,None,y_min*0.99,y_max*1.01])
    # print(l_2.get_label())
    l_1.append(l_2)
    labels = [l.get_label() for l in l_1]
    ax1.legend(l_1, labels)
    plt.savefig('ddl2interrupt.png')