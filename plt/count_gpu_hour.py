import os
import time
from datetime import datetime

log_dirs = ['../exp_1', '../exp_1_remake', '../exp_2', '../exp_2_remake', '../exp_3']

def process_file(file):
    if '.log' not in file:
        return 0

    start_line = os.popen('head -n 1 {}'.format(file)).read()
    # print(start_line)
    start_t = start_line.split(',')[0].strip()
    # print(start_t)
    start_dt = datetime.strptime(start_t, "%Y-%m-%d %H:%M:%S")
    # print(start_dt)
    start_time_stamp = time.mktime(start_dt.timetuple())
    # print(start_time_stamp)

    last_line = os.popen('tail -n 1 {}'.format(file)).read()
    # print(last_line)
    last_t = last_line.split(',')[0].strip()
    # print(last_t)
    last_dt = datetime.strptime(last_t, "%Y-%m-%d %H:%M:%S")
    # print(last_dt)
    last_time_stamp = time.mktime(last_dt.timetuple())
    # print(last_time_stamp)
    
    print(file, (last_time_stamp - start_time_stamp)/3600)
    return (last_time_stamp - start_time_stamp)/3600



if __name__ == '__main__':
    gpu_hours = 0
    for log_dir in log_dirs:
        for root, dirs, files in os.walk(log_dir, topdown=False):
            for name in files:
                gpu_hours += process_file(os.path.join(root, name))
    
    print(gpu_hours)