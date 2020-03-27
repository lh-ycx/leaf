import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
from math import log
import re
import sys

ddls = [70,170,270,520,1020,2020,4020]
log_dir = '../exp_2/interrupt/'

if __name__ == "__main__":
    for ddl in ddls:
        with open('{}femnist_interrupt_{}.cfg.log'.format(log_dir, ddl), 'r') as f:
            total = 1800
            online = 0
            min_online_fraction = 1.0
            max_online_fraction = 0.0
            for line in f:
                if 'clients online' in line:
                    online = int(line.split()[7])
                    online_fraction = online/total
                    min_online_fraction = min(min_online_fraction, online_fraction)
                    max_online_fraction = max(max_online_fraction, online_fraction)
            print(min_online_fraction, max_online_fraction)
    