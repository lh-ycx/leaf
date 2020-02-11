import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log

Es = [1,5,20]
colors = ['blue', 'green', 'orange']
log_dir = '../models/'

if __name__ == "__main__":
    plt.figure()
    cnt = 0
    for E in Es:
        with open('{}reddit_trace_{}.log'.format(log_dir, E), 'r') as f:
            x = []
            y = []
            
            current_time = 0
            hour = 0
            suc = 0

            for line in f:
                if 'current time:' in line:
                    floats = re.findall(r'\d+\.\d+',line)
                    current_time = float(floats[0])
                if 'test_loss' in line:
                    floats = re.findall(r'\d+\.\d+',line)
                    test_loss = float(floats[0])
                    x.append(current_time/3600)
                    y.append(test_loss)
        x = np.array(x)
        y = np.array(y)
        plt.plot(x,y,color=colors[cnt])
        cnt+=1
    
    plt.grid(axis='x',color='grey',ls='--')
    x_major_locator=MultipleLocator(12)
    ax=plt.gca()
    # ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    
    plt.xlabel('time line/h')
    plt.ylabel('test loss')
    plt.legend(["E = 5, with trace", "E = 5, without trace", "E = 20, with trace", "E = 20, without trace"])
    plt.savefig('test_loss_by_time.png')