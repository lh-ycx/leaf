import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys


fractions = [0.1,0.2,0.4,0.8]
paras = [100,200,400]
targets = [40,80,160]
colors = ['blue', 'green', 'orange']
log_dir = '../exp_2_remake/fraction_abs/'
dataset = 'reddit'
if dataset == 'femnist':
    target_acc = 0.81
elif dataset == 'reddit':
    target_acc = 0.16
elif dataset == 'celeba':
    target_acc = 0.87

if __name__ == "__main__":
    for target in targets:
        cnt = 0
        plt.figure()
        for para in paras:
            for fraction in fractions:
                if target != para*fraction:
                    continue
                print("target: {}, fraction: {}, para: {}".format(target, fraction, para))
                convergence_t = -1
                convergence_r = -1
                with open('{}/{}/{}_{}_{}.cfg.log'.format(log_dir,dataset,dataset,fraction,para), 'r') as f:
                    x = []
                    y = []
                    current_time = 0
                    current_round = 0
                    hour = 0

                    for line in f:
                        if 'Round' in line:
                            current_round = int(line.split()[9])
                        if 'current time:' in line:
                            floats = re.findall(r'\d+\.\d+',line)
                            current_time = float(floats[0])
                        if 'test_accuracy' in line:
                            floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                            test_acc = float(floats[3])
                            if convergence_t <= 0 and test_acc > target_acc:
                                convergence_t = current_time
                                convergence_r = current_round
                            x.append(current_round)
                            y.append(test_acc)
                x = np.array(x)
                y = np.array(y)
                plt.plot(x,y,color=colors[cnt], linewidth=2, label = 'fraction={}, para={}'.format(fraction, para))
                cnt+=1
                print('convergence_r: {}, convergence_t: {}, final_acc: {}'.format(convergence_r,convergence_t,test_acc))
        # plt.grid(axis='x',color='grey',ls='--')
        # x_major_locator=MultipleLocator(12)
        # ax=plt.gca()
        # ax为两条坐标轴的实例
        # ax.xaxis.set_major_locator(x_major_locator)

        font = {
                'weight' : 'normal',
                'size'   : 24,
                }
        font_title = {
                'weight' : 'normal',
                'size'   : 28,
                }
        plt.title('Target = {}'.format(target), font_title)
        plt.xlabel('round num',font)
        plt.ylabel('accuracy',font)
        plt.legend(fontsize=15)
        # fig.subplots_adjust(bottom=0.15)
        plt.savefig('fraction_abs_{}.png'.format(target))