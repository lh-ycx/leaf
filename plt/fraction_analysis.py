import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys

fractions = [0.1,0.3,0.5,0.7,0.8,0.9]
colors = ['limegreen', 'orange', 'peru', 'red', 'darkred', 'black']
log_dir = '../exp_2/fraction/'

if __name__ == "__main__":
    plt.figure()
    cnt = 0
    for fraction in fractions:
        with open('{}/femnist_fraction_{}.cfg.log'.format(log_dir,fraction), 'r') as f:
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
        plt.plot(x,y,color=colors[cnt],linewidth=0.75, label = 'fraction = {}'.format(fraction))
        cnt+=1
    
    font = {
            'weight' : 'normal',
            'size'   : 20,
            }
    plt.xlabel('round num', font)
    plt.ylabel('accuracy', font)
    plt.legend()
    plt.savefig('fraction_exp_acc.png')


    plt.figure()
    cnt = 0
    for fraction in fractions:
        with open('{}/femnist_fraction_{}.cfg.log'.format(log_dir,fraction), 'r') as f:
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
        plt.plot(x,y,color=colors[cnt],linewidth=0.75, label = 'fraction = {}'.format(fraction))
        cnt+=1
    
    font = {
            'weight' : 'normal',
            'size'   : 20,
            }
    plt.xlabel('round num', font)
    plt.ylabel('loss', font)
    plt.legend()
    plt.savefig('fraction_exp_loss.png')

    plt.figure()
    cnt = 0
    x = fractions
    y = []
    for fraction in fractions:
        with open('{}/femnist_fraction_{}.cfg.log'.format(log_dir,fraction), 'r') as f:
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
            average_upload_fraction = sum(upload_fractions)/len(upload_fractions)
            y.append(average_upload_fraction)
    y = np.array(y)
    plt.plot(x,y,'X-',color='red', label='Average Upload Fraction')
    for a,b in zip(x[:-1],y[:-1]):
        plt.text(a,b, '(%.2f,%.2f)' % (a,b), ha='left', fontsize=15)
    plt.text(x[-1],y[-1], '(%.2f,%.2f)' % (x[-1],y[-1]), ha='right', fontsize=15)

    font = {
            'weight' : 'normal',
            'size'   : 20,
            }
    plt.xlabel('setting fraction value', font)
    plt.ylabel('actual fraction value', font)
    plt.legend()
    plt.savefig('fraction_set_vs_real.png')