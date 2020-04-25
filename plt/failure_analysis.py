import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from datetime import datetime
import time
from math import log
from collections import defaultdict
import re
import csv

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


def check_failure_reason(ori_d_t,ori_t_t,ori_u_t,act_d_t,act_t_t,act_u_t,ddl,avg_d_t,avg_u_t):
    if (ori_d_t+ori_t_t+ori_u_t) <= ddl and (act_d_t+act_t_t+act_u_t) > ddl:
        return 'interrupt'
    if (ori_d_t+ori_u_t) > 3*(avg_d_t+avg_u_t):
        return 'network'
    else:
        return 'training'


def main(E):
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
    if E == 5:
        ddls = [230, 250, 270, 290, 310, 330]
    elif E == 1:
        ddls = [40,50,60,70,80,90,100]
    for ddl in ddls:
        f.close()
        f = open('{}femnist_ddl_{}_{}_sys.csv'.format(log_dir,E, ddl), 'r')
        data = csv.DictReader(f)
        # x = []
        # x_time = []
        y = defaultdict(list)
        cur_time = 0
        cur_round = 0
        failure_cnt = {reason:0 for reason in failure_reasons}
        round_time = 0
        for row in data:
            r = int(row['round_number'])
            if r > cur_round + delta:
                # x.append(cur_round)
                cur_time += round_time*delta
                # x_time.append(cur_time/3600)
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
                reason = check_failure_reason(ori_d_t,ori_t_t,ori_u_t,act_d_t,act_t_t,act_u_t,ddl,avg_d_t,avg_u_t)
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


        
        if E == 5:
            width = 5
        elif E == 1:
            width = 2.5
        for cnt in range(len(failure_reasons)):
            plt.bar((ddl-(1-cnt)*width), height=np.mean(y[failure_reasons[cnt]]), width=width, color=colors[cnt], label=failure_reasons[cnt])
    font = {
            'weight' : 'normal',
            'size'   : 20,
            }
    # plt.grid(axis='x',color='grey',ls='--')
    # x_major_locator=MultipleLocator(20)
    # ax=plt.gca()
    # ax为两条坐标轴的实例
    # ax.xaxis.set_major_locator(x_major_locator)
    plt.xlabel('ddl/s',font)
    plt.xticks(ddls)
    plt.ylabel('failure num',font)
    plt.title('Femnist (E = {})'.format(E), fontsize=25)
    # texts = []
    # for ddl in ddls:
    #     texts += [reason+'_{}'.format(ddl) for reason in failure_reasons]
    plt.legend([_ for _ in failure_reasons])
    plt.savefig('failure_analysis_{}.png'.format(E))
    

if __name__ == "__main__":
    main(1)
    main(5)