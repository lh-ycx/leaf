import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log

ddls = [30,40,50,60,70,80,90,100,110,120,150,180,300,600,1800]
log_dir = '../models/'

if __name__ == "__main__":
    plt.figure()
    plt.xlabel('ddl/s')
    plt.ylabel('efficiency (training time/total time)')
    # x = np.array(list(map(log, ddls)))
    x = np.array(ddls)
    y = []
    for ddl in ddls:
        with open('{}reddit_{}.log'.format(log_dir, ddl), 'r') as f:
            train_time = 0
            total_time = 0
            for line in f:
                if 'simulation time:' in line:
                    train_time += float(line.split()[-1])
                if 'current time:' in line:
                    total_time = float(line.split()[9])
            y.append(train_time/total_time)
    y = np.array(y)
    print('x:{}'.format(x))
    print('y:{}'.format(y))
    plt.plot(x,y,color='blue')
    plt.savefig('ddl2efficiency.png')