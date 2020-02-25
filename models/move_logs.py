import os
import sys


dataset = sys.argv[1]
target_dir = '../exp_1/{}/'.format(dataset)
print('target: {}'.format(target_dir))

if not os.path.isdir(target_dir):
    os.makedirs(target_dir)

os.system('mv clients_info_{}_* {}'.format(dataset, target_dir))
os.system('mv {}_* {}'.format(dataset, target_dir))
os.system('mv attended_clients_{}_* {}'.format(dataset, target_dir))
os.system('mv metrics/{}_* {}'.format(dataset, target_dir))