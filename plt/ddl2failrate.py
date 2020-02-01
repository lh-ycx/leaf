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
    plt.ylabel('fail rate')
    # x = np.array(list(map(log, ddls)))
    x = np.array(ddls)
    y = []
    for ddl in ddls:
        with open('{}reddit_{}.log'.format(log_dir, ddl), 'r') as f:
            suc = 0
            fail = 0
            for line in f:
                if 'round succeed' in line:
                    suc+=1
                if 'round failed' in line:
                    fail+=1
            y.append(fail/(fail+suc))
    y = np.array(y)
    print('x:{}'.format(x))
    print('y:{}'.format(y))
    plt.plot(x,y,color='blue')
    plt.savefig('ddl2failrate.png')