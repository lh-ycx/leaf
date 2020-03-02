#coding=utf-8

import os
import glob
import json
import multiprocessing
import shutil
import time
import xml.etree.cElementTree as et
import traceback

import fcntl # lock

ROOT_DIR = '/home/ubuntu/storage/ycx/final_trace'
OUTPUT_DIR = 'mapper_output'

PROCESS_NUM = 20
HASH_SEED = 200

meta_lst = ['guid', 'language', 'model', 'nation', 'os_lang', 'os_version', 'package_name']

def __group_by_id(input_dir, filename):
    input_file = os.path.join(ROOT_DIR, input_dir, filename)
    f = open(input_file, 'r')
    for line in f:
        raw_data = json.loads(line)
        processed_data = {}
        # process meta data
        for meta in meta_lst:
            processed_data[meta] = raw_data['__common__'][meta]
        
        # process trace
        trace_str = raw_data['extra']['data']
        trace = json.loads(trace_str)
        p = trace['network_trace'].find('download')
        trace['network_trace'] = trace['network_trace'][:p] # 去掉无用的网速
        trace.pop('phone_trace')
        trace.pop('device_model')
        processed_data['trace'] = json.dumps(trace)

        guid = raw_data['__common__']['guid']
        key = hash(guid)
        file_id = int(key) % HASH_SEED
        time_str = trace['time']
        with open('{}/{}_mapres.txt'.format(OUTPUT_DIR, file_id), 'a') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.write('{}\t{}\t{}'.format(guid, time_str, json.dumps(processed_data)) + '\r\n')
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def map():
    print('Mapping...')
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    else:
        os.system('rm {}/*'.format(OUTPUT_DIR))
    
    input_dirs = os.listdir(ROOT_DIR)
    for input_dir in input_dirs:
        if 'cdate=' not in input_dir:
            print('ignore {}'.format(input_dir))
            continue
        
        start = time.time()
        print('process data in {} at {}'.format(input_dir, start))
        pool = multiprocessing.Pool(processes = PROCESS_NUM)
        files = os.listdir(os.path.join(ROOT_DIR, input_dir))
        for f in files:
            pool.apply_async(__group_by_id, (input_dir, f, ))

        pool.close()
        pool.join()
        print('Done Post in {} seconds.'.format(time.time() - start))


def main():
    map()


if __name__ == '__main__':
    main()
