import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys

nations = ['br', 'co', 'id']
prefixs = ['ideal', 'olaf', 'real']
colors = ['blue', 'green', 'orange']
log_dir = '../models/'

if __name__ == "__main__":
    for nation in nations:
        plt.figure()
        cnt = 0
        acc = []
        for prefix in prefixs:
            with open('{}/realword_{}_{}.cfg.log'.format(log_dir,nation,prefix), 'r') as f:
                x = []
                y = []
                
                current_round = 0
                final_acc = 0
                hour = 0
                suc = 0

                for line in f:
                    if 'Round' in line:
                        current_round = int(line.split()[9])
                    if 'test_accuracy' in line:
                        floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                        test_acc = float(floats[3])
                        final_acc = test_acc
                        x.append(current_round)
                        y.append(test_acc)
            acc.append(final_acc)
            x = np.array(x)
            y = np.array(y)
            plt.plot(x,y,color=colors[cnt],linewidth=2)
            cnt+=1
        
        print('{} acc: {}'.format(nation,acc))
        print(acc[0]/acc[2], acc[1]/acc[2])
        font = {
                'weight' : 'normal',
                'size'   : 23,
                }
        plt.xlabel('round num', font)
        plt.ylabel('accuracy', font)
        plt.legend(["no trace", 
                    "randomly sample", 
                    "exactly match"], fontsize=18)
        font = {
                'weight' : 'normal',
                'size'   : 30,
                }
        plt.title(nation, font)
        plt.savefig('realworld_{}_acc_by_round.png'.format(nation))