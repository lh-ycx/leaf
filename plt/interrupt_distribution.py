import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import json
import os
from math import log

input_dir = '../trace_util/'

with open(os.path.join(input_dir, 'interrupt_type2cnt.json'), 'r') as f:
    interrupt_type2cnt = json.load(f)

plt.figure()
fig, ax = plt.subplots()
data = []
for key in interrupt_type2cnt:
    data.append(interrupt_type2cnt[key])
ax.boxplot(data, notch=True, showfliers=False)
font = {
        'weight' : 'normal',
        'size'   : 11,
        }
ax.set_xticklabels(interrupt_type2cnt.keys(),font)
# plt.hist(data, bins=100, normed=0, facecolor="blue", alpha=0.7)
font = {
    'weight' : 'normal',
    'size'   : 17,
    }
plt.title('interruption Distribution',font)
# plt.xlabel('settings')
# plt.ylabel('number of clients')

plt.ylabel('Times',font)
# fig.subplots_adjust(bottom=0.3)
plt.savefig('interrupt_distribution.png')
