import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log
import json

log_dir = '../exp_1_remake/'
colors = ['blue', 'green', 'orange']
Es = [1,5,20]

if __name__ == "__main__":
    plt.rcParams['figure.figsize'] = (15.0,7.0)
    # fig, ax = plt.subplots(figsize=(1,1))    
    # plt.figure(dpi=500, figsize=(20, 6))
    with open('{}/reddit/clients_info_reddit_no_trace_5.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data.sort()
        length = len(data)
        print('top 30% clients contribute to {} computations.'.format(sum(data[-int(0.3*length):])/sum(data)))
        data_1 = np.array(data)
        max_no_trace = np.percentile(data_1,95)
        var_no_trace = np.var(data_1)
        median_no_trace = np.percentile(data_1, 50)
    with open('{}/reddit/clients_info_reddit_trace_5.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data.sort()
        length = len(data)
        print('top 30% clients contribute to {} computations.'.format(sum(data[-int(0.3*length):])/sum(data)))
        data_2 = np.array(data)
        max_trace = np.percentile(data_2,95)
        var_trace = np.var(data_2)
        median_trace = np.percentile(data_2, 50)
        print('reddit max: ', max_no_trace, max_trace, max_trace/max_no_trace - 1)
        print('reddit var: ', var_no_trace, var_trace, var_trace/var_no_trace - 1)
        print('reddit median: ', median_no_trace, median_trace, 1-median_trace/median_no_trace)
        median = np.percentile(data_2, 50)
        acc = []
        inactive_acc = []
        for key in client2comp:
            acc.append(float(client2comp[key]['acc'][0]))
            comp = int(client2comp[key]['comp'])/10
            if comp <= median:
                inactive_acc.append(float(client2comp[key]['acc'][0]))
        print('reddit clients\' acc: {}'.format(np.mean(acc)))
        print('reddit in-active clients\' acc: {}'.format(np.mean(inactive_acc)))
        print(1-np.mean(inactive_acc)/np.mean(acc))
    with open('{}/celeba/clients_info_celeba_no_trace_1.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data.sort()
        length = len(data)
        print('top 30% clients contribute to {} computations.'.format(sum(data[-int(0.3*length):])/sum(data)))
        data_3 = np.array(data)
        max_no_trace = np.percentile(data_3,95)
        var_no_trace = np.var(data_3)
        median_no_trace = np.percentile(data_3, 50)
    with open('{}/celeba/clients_info_celeba_trace_1.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/10)
        data.sort()
        length = len(data)
        print('top 30% clients contribute to {} computations.'.format(sum(data[-int(0.3*length):])/sum(data)))
        data_4 = np.array(data)
        max_trace = np.percentile(data_4,95)
        var_trace = np.var(data_4)
        median_trace = np.percentile(data_4, 25)
        print('celeba max: ', max_no_trace, max_trace, max_trace/max_no_trace - 1)
        print('celeba var: ', var_no_trace, var_trace, var_trace/var_no_trace - 1)
        print('celeba median: ', median_no_trace, median_trace, 1-median_trace/median_no_trace)
        median = np.percentile(data_4, 50)
        acc = []
        inactive_acc = []
        for key in client2comp:
            acc.append(float(client2comp[key]['acc']))
            comp = int(client2comp[key]['comp'])/10
            if comp <= median:
                inactive_acc.append(float(client2comp[key]['acc']))
        print('celeba clients\' acc: {}'.format(np.mean(acc)))
        print('celeba in-active clients\' acc: {}'.format(np.mean(inactive_acc)))
        print(1-np.mean(inactive_acc)/np.mean(acc))
    with open('{}/femnist/clients_info_femnist_no_trace_1.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/1000)
        data.sort()
        length = len(data)
        print('top 30% clients contribute to {} computations.'.format(sum(data[-int(0.3*length):])/sum(data)))
        data_5 = np.array(data)
        max_no_trace = np.percentile(data_5,95)
        var_no_trace = np.var(data_5)
        median_no_trace = np.percentile(data_5, 50)
    with open('{}/femnist/clients_info_femnist_trace_1.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/1000)
        data.sort()
        length = len(data)
        print('top 30% clients contribute to {} computations.'.format(sum(data[-int(0.3*length):])/sum(data)))
        data_6 = np.array(data)
        max_trace = np.percentile(data_6,95)
        var_trace = np.var(data_6)
        median_trace = np.percentile(data_6, 50)
        print('femnist max: ', max_no_trace, max_trace, max_trace/max_no_trace - 1)
        print('femnist var: ', var_no_trace, var_trace, var_trace/var_no_trace - 1)
        print('femnist median: ', median_no_trace, median_trace, 1-median_trace/median_no_trace)
        median = np.percentile(data_6, 10)
        acc = []
        inactive_acc = []
        for key in client2comp:
            acc.append(float(client2comp[key]['acc']))
            comp = int(client2comp[key]['comp'])/10
            if comp <= median:
                inactive_acc.append(float(client2comp[key]['acc']))
        print('femnist clients\' acc: {}'.format(np.mean(acc)))
        print('femnist in-active clients\' acc: {}'.format(np.mean(inactive_acc)))
        print(1-np.mean(inactive_acc)/np.mean(acc))
    with open('{}/realworld_co/clients_info_realworld_co_5_no_trace.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/30)
        data.sort()
        length = len(data)
        print('top 30% clients contribute to {} computations.'.format(sum(data[-int(0.3*length):])/sum(data)))
        data_7 = np.array(data)
        max_no_trace = np.percentile(data_1,95)
        var_no_trace = np.var(data_1)
        median_no_trace = np.percentile(data_1, 50)
    with open('{}/realworld_co/clients_info_realworld_co_5_trace.cfg.json'.format(log_dir), 'r') as f:
        client2comp = json.load(f)
        data = []
        for key in client2comp:
            data.append(int(client2comp[key]['comp'])/30)
        data.sort()
        length = len(data)
        print('top 30% clients contribute to {} computations.'.format(sum(data[-int(0.3*length):])/sum(data)))
        data_8 = np.array(data)
        max_trace = np.percentile(data_8,95)
        var_trace = np.var(data_8)
        median_trace = np.percentile(data_8, 50)
        print('realworld_co max: ', max_no_trace, max_trace, max_trace/max_no_trace - 1)
        print('realworld_co var: ', var_no_trace, var_trace, var_trace/var_no_trace - 1)
        print('realworld_co median: ', median_no_trace, median_trace, 1-median_trace/median_no_trace)
        median = np.percentile(data_8, 50)
        acc = []
        inactive_acc = []
        for key in client2comp:
            acc.append(float(client2comp[key]['acc'][0]))
            comp = int(client2comp[key]['comp'])/10
            if comp <= median:
                inactive_acc.append(float(client2comp[key]['acc'][0]))
        print('realworld_co clients\' acc: {}'.format(np.mean(acc)))
        print('realworld_co in-active clients\' acc: {}'.format(np.mean(inactive_acc)))
        print(1-np.mean(inactive_acc)/np.mean(acc))
    fig, ax = plt.subplots()
    bplot = ax.boxplot([data_1,data_2,data_3,data_4,data_5,data_6,data_7,data_8],patch_artist = True, notch=True, showfliers=False)
    # print(bplot)
    colors = ['pink', 'pink', 'lightblue', 'lightblue', 'lightgreen', 'lightgreen', 'orange', 'orange']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_fc(color)
    font = {
        'weight' : 'normal',
        'size'   : 15,
        }
    ax.set_xticklabels(["reddit\n hete-unaware", 
                        "reddit\n hete-aware", 
                        "celeba\n hete-unaware", 
                        "celeba\n hete-aware",
                        "femnist\n hete-unaware",
                        "femnist\n hete-aware",
                        "realwolrd\n hete-unaware",
                        "realwolrd\n hete-aware"],font)
    # plt.hist(data, bins=100, normed=0, facecolor="blue", alpha=0.7)
    font = {
        'weight' : 'normal',
        'size'   : 26,
        }
    plt.title('Computation Distribution',font)
    # plt.xlabel('settings')
    # plt.ylabel('number of clients')
    
    plt.ylabel('relative computation',fontsize=22)
    # fig.subplots_adjust(bottom=0.15)
    plt.savefig('computation_distribution.png')


           
