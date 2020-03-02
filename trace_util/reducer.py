#coding=utf-8
"""
每个user 一个json，json里包括user的信息，然后加个字段是posts，是一个列表，里面是他所有
发过的post，再加个字段是badges，也是一个列表，里面是他所有获得的badges，每个user的json
 dump成一行写到最后结果里
"""
import os
import glob
import json
import multiprocessing
import shutil
import time
import xml.etree.cElementTree as et
import traceback

import fcntl # lock
from operator import itemgetter
from itertools import groupby

INPUT_DIR = 'mapper_output'
OUTPUT_DIR = 'reduce_result'

PROCESS_NUM = 20
HASH_SEED = 200

meta_lst = ['guid', 'language', 'model', 'nation', 'os_lang', 'os_version', 'package_name']

def reducer(file_id):
    os.system("sort -t '\t' {}/{}_mapres.txt > {}/{}_sortres.txt".format(INPUT_DIR,file_id,OUTPUT_DIR,file_id))
    f_res = open('{}/guid2data_{}.json'.format(OUTPUT_DIR, file_id), 'w')

    with open('{}/{}_sortres.txt'.format(OUTPUT_DIR, file_id)) as f:
        cur_guid = None
        guid2data = {}
        for line in f:
            guid, time, data = line.strip().split('\t')
            data = json.loads(data)
            if cur_guid is None or guid != cur_guid:
                cur_guid = guid
                guid2data[cur_guid] = {}
                guid2data[cur_guid]['trace'] = []
                for meta in meta_lst:
                    guid2data[cur_guid][meta] = data[meta]
            trace = json.loads(data['trace'])
            guid2data[cur_guid]['trace'].append(trace)
    json.dump(guid2data, f_res, indent=2)        
    f_res.close()
    print('finish reducing file No.{}'.format(file_id))

def mycallback(process_id):
    print('finish process')

def reduce():
    print('Reducing...')
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    else:
        os.system('rm {}/*'.format(OUTPUT_DIR))

    start = time.time()
    pool = multiprocessing.Pool(processes = PROCESS_NUM)
    for file_id in range(0, HASH_SEED):
        pool.apply_async(reducer, (file_id, ))
    pool.close()
    pool.join()
    os.system('rm {}/*_sortres.txt'.format(OUTPUT_DIR))
    print('Done in {} seconds.'.format(time.time() - start))

def main():
    reduce()


if __name__ == '__main__':
    main()
