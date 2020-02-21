import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# x-axis : data sample num
# y-axis : average relative comp

clients_info_dir = '../models/'
stat_dir = '../models/metrics/'
Es = [1,5,20]
dataset = 'celeba'
batch_sizee = 10

if __name__ == "__main__":
    for E in Es:
        plt.figure()
        num_samples2device_num = defaultdict(list)
        with open('{}clients_info_{}_trace_{}.cfg.json'.format(clients_info_dir, dataset, E), 'r') as f:
            clients_info = json.load(f)
        with open('{}{}_trace_{}_stat.csv'.format(stat_dir, dataset, E), 'r') as f:
            lines = f.readlines()
            lines.reverse()
            last_round = int(lines[0].split(',')[1])
            for line in lines:
                r = int(line.split(',')[1])
                if r < last_round:
                    break
                sample_num = line.split(',')[3]
                c_id = line.split(',')[0]
                comp = clients_info[c_id]['comp']
                num_samples2device_num[sample_num].append(comp)
        # x,y = [],[]
        for key in num_samples2device_num:
            train_sample = int(key)*0.8
            x = train_sample
            average_comp = sum(num_samples2device_num[key])/len(num_samples2device_num[key])
            y = average_comp/((train_sample-1)//batch_sizee + 1)
            plt.bar(x,y,width=0.25,label=key,color='b')
            
        with open('{}clients_info_{}_no_trace_{}.cfg.json'.format(clients_info_dir, dataset, E), 'r') as f:
            clients_info = json.load(f)
        with open('{}{}_no_trace_{}_stat.csv'.format(stat_dir, dataset, E), 'r') as f:
            lines = f.readlines()
            lines.reverse()
            last_round = int(lines[0].split(',')[1])
            for line in lines:
                r = int(line.split(',')[1])
                if r < last_round:
                    break
                sample_num = line.split(',')[3]
                c_id = line.split(',')[0]
                comp = clients_info[c_id]['comp']
                num_samples2device_num[sample_num].append(comp)
        for key in num_samples2device_num:
            train_sample = int(key)*0.8
            x = train_sample + 0.25
            average_comp = sum(num_samples2device_num[key])/len(num_samples2device_num[key])
            y = average_comp/((train_sample-1)//batch_sizee + 1)
            plt.bar(x,y,width=0.25,label=key,color='r')

        # x,y = [],[]
        plt.ylabel('upload times')
        plt.xlabel('sample num')
        color = ['blue', 'red']
        labels = ['trace', 'no trace']
        patches = [ mpatches.Patch(color=color[i], label="{}".format(labels[i]) ) for i in range(len(color)) ] 
        plt.legend(handles=patches, ncol=2)
        plt.title("comp_detail_{}_{}".format(dataset,E))
        plt.savefig("comp_detail_{}_{}.png".format(dataset,E))
            
    