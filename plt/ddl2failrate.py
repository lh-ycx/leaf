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
    ax2.set_ylabel('Convergence Time/s')
    # x = np.array(list(map(log, ddls)))
    x = np.array(ddls)
    y = []
    x2 = []
    y2 = []
    y_min = 9999999.0
    y_max = 0.0
    for ddl in ddls:
        with open('{}reddit_ddl_{}.cfg.log'.format(log_dir, ddl), 'r') as f:
            suc = 0
            fail = 0
            convergence_flag = False
            for line in f:
                if 'round succeed' in line:
                    suc+=1
                if 'round failed' in line:
                    fail+=1
                if 'current time' in line:
                    floats = re.findall(r'\d+\.\d+',line)
                    current_time = float(floats[0])
                if 'test_accuracy' in line:
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_acc = float(floats[0])
                    if test_acc > 0.1:
                        print(ddl, current_time)
                        x2.append(ddl)
                        y2.append(current_time)
                        convergence_flag = True
                        y_max = max(current_time,y_max)
                        y_min = min(current_time,y_min)
                        break
            y.append(fail/(fail+suc))
            if convergence_flag == False:
                x2.append(ddl)
                y2.append(100000)
    y = np.array(y)
    print('x:{}'.format(x))
    print('y:{}'.format(y))
    l_1 = ax1.plot(x,y,'o-',color='blue',label='Round Fail rate')
    l_2 = ax2.plot(x2,y2,'X-',color='red', label='Convergence Time')
    ax2.axis([None,None,y_min*0.99,y_max*1.01])
    ls = l_1 + l_2
    labels = [l.get_label() for l in ls]
    ax1.legend(ls, labels)
    fig.subplots_adjust(right=0.85)
    plt.savefig('ddl2failrate.png')