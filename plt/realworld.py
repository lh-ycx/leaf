import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys

prefixs = ['no_trace_', 'olaf_', 'real_world_']
colors = ['blue', 'green', 'orange']
nation = sys.argv[1]
log_dir = '../exp_realworld/{}/'.format(nation)

if __name__ == "__main__":
    plt.figure()
    cnt = 0
    for prefix in prefixs:
        with open('{}/{}{}.cfg.log'.format(log_dir,prefix,nation), 'r') as f:
            x = []
            y = []
            
            current_round = 0
            hour = 0
            suc = 0

            for line in f:
                if 'Round' in line:
                    current_round = int(line.split()[9])
                if 'test_accuracy' in line:
                    if current_round % 50 != 0:
                        continue
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_acc = float(floats[0])
                    if test_acc > 1:
                        print(floats)
                        assert False
                    x.append(current_round)
                    y.append(test_acc)
        x = np.array(x)
        y = np.array(y)
        plt.plot(x,y,color=colors[cnt],linewidth=0.75)
        cnt+=1

    
    font = {
            'weight' : 'normal',
            'size'   : 15,
            }
    plt.xlabel('round num', font)
    plt.ylabel('accuracy', font)
    plt.legend(["no trace", 
                "olaf", 
                "real world"])
    plt.savefig('{}_acc_by_round.png'.format(nation))