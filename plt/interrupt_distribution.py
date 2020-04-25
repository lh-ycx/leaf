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
interrupt_type2cnt.pop('bettary low')
for key in interrupt_type2cnt:
    data.append(interrupt_type2cnt[key])
ax.boxplot(data, notch=True, showfliers=False)
font = {
        'weight' : 'normal',
        'size'   : 15,
        }
ax.set_xticklabels(['network change', 'charge off', 'user interaction'],font)
plt.ylabel('Times',font)
# plt.hist(data, bins=100, normed=0, facecolor="blue", alpha=0.7)
font = {
    'weight' : 'normal',
    'size'   : 20,
    }
plt.title('Interruption Reasons',font)
# plt.xlabel('settings')
# plt.ylabel('number of clients')
# fig.subplots_adjust(bottom=0.3)
plt.savefig('interrupt_distribution.png')
