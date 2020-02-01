import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from datetime import datetime
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
            yy = []
            
            current_time = 0
            suc_r = 0
            most_suc_r = 0
            fail_r = 0
            most_fail_r = 0

            for line in f:
                if 'current time:' in line:
                    floats = re.findall(r'\d+\.\d+',line)
                    current_time = float(floats[0])/3600
                if 'clients online' in line:
                    tot = int(line.split()[7])
                    tot = min(tot, 50)
                if ' upload ' in line:
                    if 'at most' in line:
                        most = int(line.split()[7])
                        upload_rate = most/tot
                        # if upload_rate > 1.0:
                            # upload_rate = 1.0
                        if upload_rate >= 0.8:
                            most_suc_r+=1
                        else:
                            most_fail_r+=1
                        yy.append(upload_rate)
                    else:
                        suc = int(line.split()[7])
                        tot = int(line.split()[9])
                        upload_rate = suc/tot
                        if upload_rate >= 0.8:
                            suc_r+=1
                        else:
                            fail_r+=1
                        x.append(current_time)
                        y.append(upload_rate)
                if 'insufficient' in line:
                    x.append(current_time)
                    y.append(0.5)
                    yy.append(0.5)


        plt.figure()
        plt.grid(axis='x',color='grey',ls='--')
        plt.xlabel('Time Line')
        plt.ylabel('upload rate')
        x_major_locator=MultipleLocator(24)
        ax=plt.gca()
        #ax为两条坐标轴的实例
        ax.xaxis.set_major_locator(x_major_locator)
        #分割线
        plt.hlines(0.8, 0, max(x), color="red")
        x = np.array(x)
        y = np.array(y)
        yy = np.array(yy)
        plt.title('upload_rate_{}'.format(ddl))
        # plt.plot(x,y,linewidth=0.4,color='blue')
        # plt.plot(x,yy,linewidth=0.5,color='green')
        plt.plot(x,y,color='blue')
        plt.plot(x,yy,color='green')
        plt.legend(["random selection","best selection"])
        plt.savefig('upload_rate_{}.png'.format(ddl))
        
        print('----------------- ddl: {} -----------------'.format(ddl))
        print('suc round: {}, fail round: {}, suc rate: {}'.format(suc_r, fail_r, suc_r/(suc_r+fail_r)))
        print('most suc round: {}, most fail round: {}, most suc rate: {}'.format(most_suc_r, most_fail_r, most_suc_r/(most_suc_r+most_fail_r)))
