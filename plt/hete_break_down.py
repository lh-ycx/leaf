import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log
import sys
import json
import csv
from collections import defaultdict


colors = ['green', 'orange', 'blue', 'brown']
log_dir = '../exp_1_remake/hete/'
datasets = ['realworld_co','femnist']
prefixs = ['unaware','hard','behav','aware']

def check_failure_reason(ori_d_t,ori_t_t,ori_u_t,act_d_t,act_t_t,act_u_t,ddl,avg_d_t,avg_u_t):
    if (ori_d_t+ori_t_t+ori_u_t) <= ddl and (act_d_t+act_t_t+act_u_t) > ddl:
        return 'interruption'
    if (ori_d_t+ori_u_t) > 3*(avg_d_t+avg_u_t):
        return 'network'
    else:
        return 'training'

if __name__ == "__main__":
    # acc_time curve
    for dataset in datasets:
        if dataset == 'femnist':
            target_acc = 0.81
        elif dataset == 'reddit' or dataset == 'realworld_co':
            target_acc = 0.09
        elif dataset == 'celeba':
            target_acc = 0.87
        
        plt.figure()
        fig,ax1 = plt.subplots(figsize=(6.5, 4))
        cnt = 0
        for prefix in prefixs:
            file = '{}/hete_{}_{}.cfg.log'.format(log_dir,prefix,dataset)
            
            with open(file, 'r') as f:
                x = []
                y = []
                
                current_time = 0
                hour = 0
                suc = 0
                convergence_t = -1

                for line in f:
                    if 'current time:' in line:
                        floats = re.findall(r'\d+\.\d+',line)
                        current_time = float(floats[0])
                    if 'test_accuracy' in line:
                        floats = re.findall(r'\d+\.\d*e*-*\d*',line)
                        test_acc = float(floats[0])
                        if convergence_t <= 0 and test_acc > target_acc:
                            convergence_t = current_time
                        x.append(current_time/3600)
                        y.append(test_acc)
            x = np.array(x)
            y = np.array(y)
            plt.plot(x,y,color=colors[cnt], lw=2.5,label='heterogeneity-{}'.format(prefix))
            print('{}, hete-{}, acc: {}; convergence time: {}'.format(dataset, prefix, test_acc, convergence_t))
            cnt+=1
        
        plt.grid(axis='x',color='grey',ls='--')
        x_major_locator=MultipleLocator(6)
        ax=plt.gca()
        # ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        
        font = {
                'weight' : 'normal',
                'size'   : 24,
                }
        font_title = {
                'weight' : 'normal',
                'size'   : 28,
                }
        '''
        if dataset == 'realworld_co':
            plt.title('M-Type', font_title)
        else:
            plt.title('{}'.format(dataset), font_title)
        plt.xlabel('time line/h',font)
        plt.ylabel('accuracy',font)
        plt.legend(fontsize=13)
        '''
        if dataset == 'realworld_co':
            plt.xlim([0,19])
        if dataset == 'femnist' :
            plt.xlim([0,13])
        plt.tick_params(labelsize=16)
        # fig.subplots_adjust(bottom=0.15)
        plt.savefig('hete_acc_{}.pdf'.format(dataset))
    

    # participation bias
    for dataset in datasets:
        datas = []
        for prefix in prefixs:
            with open('{}/clients_info_hete_{}_{}.cfg.json'.format(log_dir,prefix,dataset), 'r') as f:
                client2comp = json.load(f)
                data = []
                for key in client2comp:
                    if dataset == 'femnist':
                        data.append(int(client2comp[key]['comp'])/100)
                    else:
                        data.append(int(client2comp[key]['comp'])/10)
                data.sort()
                datas.append(data)
                length = len(data)
                print('{}, {}:top 30% clients contribute to {} computations.'.format(dataset, prefix, sum(data[-int(0.3*length):])/sum(data)))
        
        fig, ax = plt.subplots()
        bplot = ax.boxplot(datas, patch_artist = True, notch=True, showfliers=False)
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_fc('gray')
        font = {
            'weight' : 'normal',
            'size'   : 15,
            }
        # ax.set_xticklabels(["hete-{}".format(_) for _ in prefixs],font)
        ax.set_xticklabels(['' for _ in prefixs],font)
        plt.tick_params(labelsize=16)
        # plt.hist(data, bins=100, normed=0, facecolor="blue", alpha=0.7)
        font = {
            'weight' : 'normal',
            'size'   : 26,
            }
        '''
        if dataset == 'realworld_co':
            plt.title('M-Type',font)
        else:
            plt.title(dataset,font)
        '''
        # plt.xlabel('settings')
        # plt.ylabel('number of clients')
        
        # plt.ylabel('relative computation',fontsize=22)
        # plt.xticks(rotation=30)
        # fig.subplots_adjust(bottom=0.25)
        # if dataset == 'femnist':
        #     fig.subplots_adjust(left=0.15)
        plt.savefig('hete_comp_{}.pdf'.format(dataset))


    # acc cdf
    for dataset in datasets:
        plt.figure()
        fig, ax = plt.subplots()
        cnt = 0
        for prefix in prefixs:
            file_dir = '{}/clients_info_hete_{}_{}.cfg.json'.format(log_dir,prefix,dataset)
            with open(file_dir, 'r') as f:
                client2acc = json.load(f)
                data = []
                for key in client2acc:
                    if dataset =='reddit' or dataset =='realworld_co':
                        data.append((client2acc[key]['acc'])[0])
                    else:
                        data.append((client2acc[key]['acc']))
                count = len(data)
                data.sort()
                x=[]
                y=[]
                for i in range(count):
                    x.append(data[i])
                    y.append((i+1)/count)
                median = np.percentile(x,50)
                plt.plot(x,y,lw=2.5,color=colors[cnt],label='Hete-{}'.format(prefix))
                cnt+=1
                print('{}, hete-{}: median_acc={}'.format(dataset, prefix, median))
        '''
        plt.xlabel('Accuracy', fontsize=20)
        plt.legend(fontsize=20)
        if dataset == 'realworld_co':
            plt.title('M-Type', fontsize=25)
        else:
            plt.title(dataset, fontsize=25)    
        plt.ylabel('CDF', fontsize=20)
        '''
        # fig.subplots_adjust(bottom=0.3)
        if dataset == 'reddit' or dataset == 'realworld_co':
            plt.xlim([0.02,0.17])
        else:
            plt.xlim([0.4,1.01])
        plt.tick_params(labelsize=16)
        # fig.subplots_adjust(bottom=0.15)
        plt.savefig('hete_acc_cdf_{}.pdf'.format(dataset))



    # failure analysis
    failure_reasons = ['network', 'training', 'interruption']
    delta = 5
    for dataset in datasets:
        f = open('{}/hete_aware_{}_sys.csv'.format(log_dir,dataset), 'r')
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
        fig,ax1 = plt.subplots()
        bar_num = 0
        for prefix in prefixs:
            bar_num+=1
            if dataset == 'femnist':
                ddl = 310
            if dataset == 'realworld_co':
                ddl = 85
            if prefix == 'unaware':
                ddl = 10000000
            f.close()
            f = open('{}/hete_{}_{}_sys.csv'.format(log_dir,prefix,dataset), 'r')
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

            width = 10
            ls = []
            bottom = 0
            colors = ['white', 'gray', 'black']
            for cnt in range(len(failure_reasons)):
                l = plt.bar(bar_num*width, height=np.mean(y[failure_reasons[cnt]]), width=0.6*width, bottom=bottom, facecolor=colors[cnt], label=failure_reasons[cnt], edgecolor='black')
                ls.append(l)
                bottom+=np.mean(y[failure_reasons[cnt]])
            plt.text(bar_num*width, bottom+0.05,'{:.1f}'.format(bottom),ha='center', va= 'bottom',fontsize=15)
        font = {
                'weight' : 'normal',
                'size'   : 20,
                }
        # plt.grid(axis='x',color='grey',ls='--')
        # x_major_locator=MultipleLocator(20)
        # ax=plt.gca()
        # ax为两条坐标轴的实例
        # ax.xaxis.set_major_locator(x_major_locator)
        # plt.xlabel('',font)
        ax1.set_xticks([(cnt+1)*width for cnt in range(len(prefixs))])
        # ax1.set_xticklabels(['hete-{}'.format(prefix) for prefix in prefixs])
        ax1.set_xticklabels(['' for prefix in prefixs])
        '''
        plt.ylabel('% of failure clients',font)
        if dataset == 'realworld_co':
            plt.title('M-Type', fontsize=25)
        else:
            plt.title(dataset, fontsize=25)
        ''' 
        # texts = []
        # for ddl in ddls:
        #     texts += [reason+'_{}'.format(ddl) for reason in failure_reasons]
        # plt.legend(ls, [_ for _ in failure_reasons])
        # plt.legend([l1], ["ddl corresonping to the shortest convergence time"])
        # plt.legend()
        plt.tick_params(labelsize=16)
        if dataset == 'femnist':
            plt.ylim([0,9])
        else:
            plt.ylim([0,17.5])
        plt.savefig('hete_failure_{}.pdf'.format(dataset))