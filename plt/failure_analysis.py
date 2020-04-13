import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from datetime import datetime
import time
from math import log
from collections import defaultdict
import re
import csv

ddls = [250, 310]
delta = 5
log_dir = '../exp_2_remake/femnist_ddl/'
failure_reasons = ['network', 'training', 'interrupt']
colors = ['blue', 'green', 'orange']
avg_d_t = 0
avg_u_t = 0
avg_t_t = 0
std_d_t = 0
std_d_t = 0
std_t_t = 0


def check_failure_reason(ori_d_t,ori_t_t,ori_u_t,act_d_t,act_t_t,act_u_t):
    if (ori_d_t+ori_t_t+ori_u_t) <= ddl and (act_d_t+act_t_t+act_u_t) > ddl:
        return 'interrupt'
    if (ori_d_t+ori_u_t) > 2*(avg_d_t+avg_u_t):
        return 'network'
    else:
        return 'training'

if __name__ == "__main__":
    f = open('{}femnist_ddl_5_310_sys.csv'.format(log_dir), 'r')
    data = csv.DictReader(f)
    d_ts, u_ts, t_ts = [], [], []
    for row in data:
        # print(row)
        d_ts.append(float(row['ori_d_t']))
        u_ts.append(float(row['ori_u_t']))
        t_ts.append(float(row['ori_t_t']))
        # break
    # print(d_ts)
    avg_d_t = np.mean(d_ts)
    avg_u_t = np.mean(u_ts)
    avg_t_t = np.mean(t_ts)
    std_d_t = np.std(d_ts)
    std_u_t = np.std(u_ts)
    std_t_t = np.std(t_ts)
    print('average download time:', avg_d_t)
    print('download time std:', std_d_t)
    print('average upload time:', avg_u_t)
    print('upload time std:', std_u_t)
    print('average train time:', avg_t_t)
    print('train time std:', std_t_t)
    
    plt.figure()
    for ddl in ddls:
        f.close()
        f = open('{}femnist_ddl_5_{}_sys.csv'.format(log_dir,ddl), 'r')
        data = csv.DictReader(f)
        x = []
        x_time = []
        y = defaultdict(list)
        cur_time = 0
        cur_round = 0
        failure_cnt = {reason:0 for reason in failure_reasons}
        round_time = 0
        for row in data:
            r = int(row['round_number'])
            if r > cur_round + delta:
                x.append(cur_round)
                cur_time += round_time*delta
                x_time.append(cur_time/3600)
                for reason in failure_reasons:
                    y[reason].append(failure_cnt[reason]/delta)
                cur_round = r
                failure_cnt = {reason:0 for reason in failure_reasons}
                round_time = 0
            
            ori_d_t = float(row['ori_d_t'])
            ori_u_t = float(row['ori_u_t'])
            ori_t_t = float(row['ori_t_t'])
            
            act_d_t = float(row['act_d_t'])
            act_u_t = float(row['act_u_t'])
            act_t_t = float(row['act_t_t'])
            round_time = min(ddl, max(round_time, act_d_t+act_t_t+act_u_t))
            round_time += 20
            if (act_d_t+act_t_t+act_u_t) > ddl:
                reason = check_failure_reason(ori_d_t,ori_t_t,ori_u_t,act_d_t,act_t_t,act_u_t)
                failure_cnt[reason] += 1
        
        '''
        x.append(cur_round)
        cur_time += round_time
        x_time.append(cur_time)
        for reason in failure_reasons:
            y[reason].append(failure_cnt[reason]/delta)
        plt.figure()
        for cnt in range(len(failure_reasons)):
            plt.plot(x,y[failure_reasons[cnt]], c=colors[cnt])
        font = {
                'weight' : 'normal',
                'size'   : 15,
                }
        plt.xlabel('round num',font)
        plt.ylabel('failure num')
        plt.legend(failure_reasons)
        plt.savefig('failure_analysis.png')
        '''


        
        for cnt in range(len(failure_reasons)):
            if ddl == 250:
                plt.plot(x_time,y[failure_reasons[cnt]], c=colors[cnt],ls='--')
            else:
                plt.plot(x_time,y[failure_reasons[cnt]], c=colors[cnt])
    font = {
            'weight' : 'normal',
            'size'   : 15,
            }
    plt.grid(axis='x',color='grey',ls='--')
    x_major_locator=MultipleLocator(12)
    ax=plt.gca()
    # ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xlabel('timeline/h',font)
    plt.ylabel('failure num',font)
    texts = []
    for ddl in ddls:
        texts += [reason+'_{}'.format(ddl) for reason in failure_reasons]
    plt.legend(texts)
    plt.savefig('failure_analysis_by_time.png')
    


    