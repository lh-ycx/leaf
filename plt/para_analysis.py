import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys

paras = [25,50,100,200,500,1000]
colors = ['limegreen', 'orange', 'peru', 'red', 'darkred', 'black']
log_dir = '../exp_2/para/'

if __name__ == "__main__":
    plt.figure()
    cnt = 0
    for para in paras:
        with open('{}/para_reddit_{}.cfg.log'.format(log_dir,para), 'r') as f:
            x = []
            y = []
            
            current_round = 0
            hour = 0
            suc = 0

            for line in f:
                if 'Round' in line:
                    current_round = int(line.split()[9])
                if 'test_accuracy' in line:
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_acc = float(floats[0])
                    if test_acc > 1:
                        print(floats)
                        assert False
                    x.append(current_round)
                    y.append(test_acc)
        x = np.array(x)
        y = np.array(y)
        plt.plot(x,y,color=colors[cnt],linewidth=0.75, label = 'para = {}'.format(para))
        cnt+=1
    
    font = {
            'weight' : 'normal',
            'size'   : 20,
            }
    plt.xlabel('round num', font)
    plt.ylabel('accuracy', font)
    plt.legend()
    plt.savefig('para_acc.png')


    plt.figure()
    cnt = 0
    for para in paras:
        with open('{}/para_reddit_{}.cfg.log'.format(log_dir,para), 'r') as f:
            x = []
            y = []
            
            current_round = 0
            hour = 0
            suc = 0

            for line in f:
                if 'Round' in line:
                    current_round = int(line.split()[9])
                if 'test_loss' in line:
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_loss = float(floats[0])
                    x.append(current_round)
                    y.append(test_loss)
        x = np.array(x)
        y = np.array(y)
        plt.plot(x,y,color=colors[cnt],linewidth=0.75, label = 'para = {}'.format(para))
        cnt+=1
    
    font = {
            'weight' : 'normal',
            'size'   : 20,
            }
    plt.xlabel('round num', font)
    plt.ylabel('loss', font)
    plt.legend()
    plt.savefig('para_loss.png')

    plt.figure()
    cnt = 0
    x = paras
    y = []
    target_acc = 0.05
    for para in paras:
        flag = True
        with open('{}/para_reddit_{}.cfg.log'.format(log_dir,para), 'r') as f:
            for line in f:
                if 'Round' in line:
                    current_round = int(line.split()[9])
                if 'test_accuracy' in line:
                    floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                    test_acc = float(floats[0])
                    if test_acc > target_acc:
                        y.append(current_round)
                        flag = False
                        break
            if flag:
                y.append(current_round)
    y = np.array(y)
    plt.plot(x,y,'X-',color='red', label='round to reach target acc')

    font = {
            'weight' : 'normal',
            'size'   : 20,
            }
    plt.xlabel('client num per round', font)
    plt.ylabel('round num', font)
    plt.legend()
    plt.savefig('para_round_to_reach_{}.png'.format(target_acc))