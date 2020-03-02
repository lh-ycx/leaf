import os
import json

state_cnt = 5   # screen, lock, battery, battery_percent, net

INPUT_DIR = 'available_trace'
HASH_SEED = 200

def zip_trace(traces):
    message = ''
    # screen, lock, battery, battery_percent, net
    states = ['screen_on', 'screen_unlock', 'battery_charged_off', '0.0%', 'Unknow']
    for trace in traces:
        t = trace['time']
        new_states = []
        new_states.append(trace['screen_trace'].strip().split()[-1])
        new_states.append(trace['screen_lock_trace'].strip().split()[-1])
        new_states.append(trace['battery_trace'].strip().split()[-2])
        new_states.append(trace['battery_trace'].strip().split()[-1])
        new_states.append(trace['network_trace'].strip().split()[-1])
        for i in range(state_cnt):
            if states[i] != new_states[i]:
                message += t + '\t' + new_states[i] + '\n'
        states = new_states
    return message
        

if __name__ == '__main__':
    zipped_guid2data = {}
    cnt = 0
    for i in range(HASH_SEED):
        print('processing available_guid2data_{}.json'.format(i))
        with open("{}/available_guid2data_{}.json".format(INPUT_DIR, i), 'r') as f:
            guid2data = json.load(f)
            for guid in list(guid2data.keys()):
                zipped_guid2data[guid] = guid2data[guid]
                zipped_guid2data[guid]['sdk_version'] = guid2data[guid]['trace'][0]['sdk_version']
                zipped_guid2data[guid]['kb_time_zone'] = guid2data[guid]['trace'][0]['kb_time_zone']
                zipped_guid2data[guid]['messages'] = zip_trace(zipped_guid2data[guid]['trace'])
                zipped_guid2data[guid].pop('trace')
                cnt+=1
                # if cnt % 100 == 0:
                    # print('processed {} users..'.format(cnt))
    
    print('total trace num: {}'.format(cnt))
    print('saving as zipped_guid2data.json')
    with open("zipped_guid2data.json", 'w') as f:
        json.dump(zipped_guid2data, f, indent=2)
    
        