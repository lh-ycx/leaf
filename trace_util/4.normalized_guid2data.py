import json
import os
import time
from datetime import datetime

input_dir = 'zipped_guid2data.json'
fmt = '%Y-%m-%d %H:%M:%S'
refer_time = '2020-01-23 00:00:00'
refer_second = time.mktime(datetime.strptime(refer_time, fmt).timetuple())

# normalize the trace - make sure the trace length is n days (n belongs to N+)

def get_time_stamp(mes):
    t = mes.strip().split("\t")[0].strip()
    time_stamp = time.mktime(datetime.strptime(t, fmt).timetuple()) - \
                time.mktime(datetime.strptime(refer_time, fmt).timetuple())
    return time_stamp

def normalize_messages(messages):
    # print('before:')
    # print(messages)
    # print(messages[-10:])
    new_messages = []
    
    st = 0
    st_mes = messages[st]
    while st_mes.strip() == '':
        st += 1
        mes = messages[st]
    st_t = st_mes.strip().split("\t")[0].strip()
    st_stamp = time.mktime(datetime.strptime(st_t, fmt).timetuple()) - \
                time.mktime(datetime.strptime(refer_time, fmt).timetuple())

    ed = -1
    ed_mes = messages[ed]
    while ed_mes.strip() == '':
        ed -= 1
        ed_mes = messages[ed]
    ed_t = ed_mes.strip().split("\t")[0].strip()
    ed_stamp = time.mktime(datetime.strptime(ed_t, fmt).timetuple()) - \
                time.mktime(datetime.strptime(refer_time, fmt).timetuple())
    
    yu = (ed_stamp - st_stamp) % 86400
    shang = (ed_stamp - st_stamp) // 86400
    # print('shang: {}'.format(shang))
    # print('yu: {}'.format(yu))

    if yu > 3600 * 20:
        new_messages = messages[st:ed+1]
        # screen on, 2g in the end of the trace
        new_messages.append(ed_t + '\t' + 'screen_on')
        new_messages.append(ed_t + '\t' + '2G')
        # extend the trace to a 'full' day
        new_ed_stamp = st_stamp + (shang+1)*86400 + \
                        time.mktime(datetime.strptime(refer_time, fmt).timetuple())
        time_tuple = time.localtime(new_ed_stamp)
        new_ed_t = time.strftime(fmt, time_tuple)  # 把时间元祖转换成格式化好的时间
        new_messages.append(new_ed_t + '\t' + 'screen_on')
        new_messages.append(new_ed_t + '\t' + '2G')
    else:
        # do not extend, abandon the extra trace
        max_time_stamp = st_stamp + shang*86400
        while(get_time_stamp(ed_mes) > max_time_stamp) :
            ed -= 1
            ed_mes = messages[ed]
        new_messages = messages[st:ed+1]
        new_ed_stamp = st_stamp + shang*86400 + \
                        time.mktime(datetime.strptime(refer_time, fmt).timetuple())
        time_tuple = time.localtime(new_ed_stamp)
        new_ed_t = time.strftime(fmt, time_tuple)  # 把时间元祖转换成格式化好的时间
        new_messages.append(new_ed_t + '\t' + 'screen_on')
        new_messages.append(new_ed_t + '\t' + '2G')
    
    # print('after:')
    # print(new_messages)
    # print(new_messages[-10:])

    return new_messages
    


if __name__ == "__main__":
    normalized_guid2data = {}
    with open(input_dir, 'r') as f:
        guid2data = json.load(f)
        cnt = 0
        for guid in list(guid2data.keys()):
            try:
                normalized_guid2data[guid] = guid2data[guid]
                messages = guid2data[guid]['messages'].split('\n')
                new_messages = normalize_messages(messages)
                guid2data[guid]['messages'] = '\n'.join(new_messages)
                cnt += 1
                if cnt % 1000 == 0:
                    print('processed {} users..'.format(cnt))
            except Exception as e:
                normalized_guid2data.pop(guid)
                print(e)
    
    with open("normalized_guid2data.json", 'w') as f:
        json.dump(normalized_guid2data, f, indent=2)

