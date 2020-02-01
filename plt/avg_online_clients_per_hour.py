import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.pyplot import MultipleLocator
import time
import re
from math import log

ddls = [30,40,50,60,70,80,90,100,110,120,150,180,300,600,1800]
log_dir = '../models/'

if __name__ == "__main__":
    
    for ddl in ddls:
        with open('{}reddit_{}.log'.format(log_dir, ddl), 'r') as f:
            x = []
            y = []
            
            current_time = 0
            hour = 1
            online_clients = []

            for line in f:
                if 'current time:' in line:
                    floats = re.findall(r'\d+\.\d+',line)
                    current_time = float(floats[0])
                    if current_time > hour*3600:
                        x.append(hour)
                        hour += 1
                        y.append(sum(online_clients)/len(online_clients))
                        online_clients = []
                if 'clients online' in line:
                    online_clients.append(int(line.split()[7]))
        plt.figure()
        plt.grid(axis='x',color='grey',ls='--')
        plt.xlabel('Time Line')
        plt.ylabel('Online Clients/hour')
        x_major_locator=MultipleLocator(24)
        ax=plt.gca()
        #ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        x = np.array(x)
        y = np.array(y)
        plt.plot(x,y,color='blue')
        plt.savefig('avg_online_clients_per_hour_{}.png'.format(ddl))