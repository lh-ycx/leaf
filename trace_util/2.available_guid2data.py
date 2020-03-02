import os
import json
import time
import multiprocessing

INPUT_DIR = 'reduce_result'
OUTPUT_DIR = 'available_trace'

PROCESS_NUM = 20
HASH_SEED = 200

day_cnt = [0] * 15

def my_call_back(res):
    for i in range(len(day_cnt)):
        day_cnt[i] += res[i]

def get_available_data(file_id):
    tmp_day_cnt = [0] * 15
    file = 'guid2data_{}.json'.format(file_id)
    print('processing {}'.format(file))
    with open(os.path.join(INPUT_DIR, file), 'r') as f:
        file_id = int(file.strip().split('_')[1].split('.')[0])
        print(file_id)
        guid2data = json.load(f)
        for guid in list(guid2data.keys()):
            try:
                st = guid2data[guid]['trace'][0]['time'].strip()
                ed = guid2data[guid]['trace'][-1]['time'].strip()
                format_str = "%Y-%m-%d %H:%M:%S"
                st_array = time.strptime(st, format_str)
                ed_array = time.strptime(ed, format_str)
                st_stamp = time.mktime(st_array)
                ed_stamp = time.mktime(ed_array)
                length = int((ed_stamp-st_stamp)//86400)
                tmp_day_cnt[length] += 1
                if length == 0:
                    guid2data.pop(guid)
            except Exception as e:
                print(e)
                guid2data.pop(guid)
        print('saving as available_guid2data_{}.json...'.format(file_id))
        with open('{}/available_guid2data_{}.json'.format(OUTPUT_DIR, file_id), 'w') as nf:
            json.dump(guid2data, nf, indent=2)

    return tmp_day_cnt



if __name__ == "__main__":
    
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    else:
        os.system('rm {}/*'.format(OUTPUT_DIR))

    start = time.time()
    pool = multiprocessing.Pool(processes = PROCESS_NUM)
    for file_id in range(0, HASH_SEED):
        pool.apply_async(get_available_data, (file_id, ), callback=my_call_back)
    pool.close()
    pool.join()
    
    print('Done in {} seconds.'.format(time.time() - start))        
    print(day_cnt)