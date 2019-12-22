import json
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import os
import pandas as pd
from collections import defaultdict
import re

log_files = ['reddit_SucFedAvg_1.log']

def print_one_log(log_file):
    t_accs = []
    t_losses = []
    test_accs = []
    test_losses = []
    with open(log_file, 'r') as f:
        lines = [line.rstrip() for line in f]
        for line in lines:
            if 'average acc:' in line:
                acc_loss = re.findall(r'\d+\.\d+',line)
                t_acc = acc_loss[0]
                t_loss = acc_loss[1]
                t_accs.append(float(t_acc))
                t_losses.append(float(t_loss))
            if 'test_accuracy:' in line:
                test_acc_loss = re.findall(r'\d+\.\d+',line)
                test_acc = test_acc_loss[0]
                test_accs.append(float(test_acc))
            if 'test_loss:' in line:
                test_acc_loss = re.findall(r'\d+\.\d+',line)
                test_loss = test_acc_loss[0]
                test_losses.append(float(test_loss))
        # print(t_accs[:5])
        # print(len(t_losses))
        
        # 1: train acc
        x = np.linspace(0, len(t_accs), len(t_accs))
        y = np.array(t_accs)
        plt.figure()
        plt.xlabel('round num')
        plt.ylabel('acc')
        plt.plot(x,y,color='red')
        plt.savefig('train_acc_{}.png'.format(log_file))
        
        # 2: train loss
        x = np.linspace(0, len(t_losses), len(t_losses))
        y = np.array(t_losses)
        plt.figure()
        plt.xlabel('round num')
        plt.ylabel('loss')
        plt.plot(x,y,color='red')
        plt.savefig('train_loss_{}.png'.format(log_file))
        
        # 3: test acc
        x = np.linspace(0, len(t_accs), len(t_accs)/10)
        y = np.array(test_accs)
        plt.figure()
        plt.xlabel('round num')
        plt.ylabel('acc')
        plt.plot(x,y,color='red')
        plt.savefig('test_acc_{}.png'.format(log_file))
        
        # 4: test loss
        x = np.linspace(0, len(t_losses), len(t_losses)/10)
        y = np.array(test_losses)
        plt.figure()
        plt.xlabel('round num')
        plt.ylabel('loss')
        plt.plot(x,y,color='red')
        plt.savefig('test_loss_{}.png'.format(log_file))
        
if __name__ == '__main__' :
    for log in log_files:
        print_one_log(log)
        