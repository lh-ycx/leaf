import os
import json


os.system('python mapper.py')
os.system('python reducer.py')

'''
root_dir = '.'
guid2data = {}
meta_lst = ['guid', 'language', 'model', 'nation', 'os_lang', 'os_version', 'package_name']

def process_line(line):
    raw_data = json.loads(line)
    guid = raw_data['__common__']['guid']
    if guid not in guid2data:
        guid2data[guid] = {}
        guid2data[guid]['trace'] = []
        for meta in meta_lst:
            guid2data[guid][meta] = raw_data['__common__'][meta]
    else:
        trace_str = raw_data['extra']['data']
        trace = json.loads(trace_str)
        p = trace['network_trace'].find('download')
        trace['network_trace'] = trace['network_trace'][:p] # 去掉无用的网速
        trace.pop('phone_trace')
        trace.pop('device_model')
        # timestamp = trace['time']
        guid2data[guid]['trace'].append(trace)


if __name__ == "__main__":
    
    line_cnt = 0
    file_cnt = 0
    for root, dirs, files in os.walk(root_dir, topdown=False):
        for ff in files:
            try:
                with open(os.path.join(root, ff),'r') as f:
                    for line in f.readlines():
                        process_line(line)
                        line_cnt+=1
                print("process {} files".format(file_cnt))
                file_cnt += 1
            except Exception as e:
                print(ff)
                print(e)
    
    print("line_cnt:{}".format(line_cnt))
    print('usr_cnt:{}'.format(len(guid2data)))
    # for guid in list(guid2data.keys())[:3]:
        # print(guid2data[guid])
        # break
    # trace 按时间排序
    def get_time(ele):
        return ele['time']
    cnt = 0
    for guid in guid2data.keys():
        guid2data[guid]['trace'].sort(key=get_time)
        cnt += 1
        if cnt % 100 == 0:
            print('processed {} user trace...'.format(cnt))
    
    with open('guid2data.json', 'w') as f:
        json.dump(guid2data, f, indent=2)
'''