import json
import time
from datetime import datetime
import random
import pandas as pd
import traceback
import sys
from collections import defaultdict
import numpy as np
from device_util.device_util import Device_Util

class Timer:
    def __init__(self, ubt, google=True):
        self.isSuccess = False
        self.fmt = '%Y-%m-%d %H:%M:%S'
        self.refer_time = '2020-01-02 00:00:00'
        self.refer_second = time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
        self.trace_start, self.trace_end = None, None
        self.ready_time = []
        self.ready_time_loose = []
        self.google = google
        self.model = ubt['model']
        self.state = ['battery_charged_off', 'battery_charged_on', 'battery_low', 'battery_okay',
                      'phone_off', 'phone_on', 'screen_off', 'screen_on', 'screen_unlock']

        # get marched ubt from user_behavior_tiny by uid
        self.ubt = ubt

        if ubt == None: # no user trace will be used
            self.isSuccess = True
            return

        # ### get ready time list ###
        start_charge, end_charge, okay, low = None, None, None, None
        message = self.ubt['messages'].split('\n')
        ready_time = []
        ready_time_loose = []
        idle = False # define: idle = locked
        screen_off = False
        locked = False 
        wifi = False
        charged = False
        battery_level = 0.0
        st = None   # ready start time
        ed = None   # ready end time
        st_loose = None
        ed_loose = None
        for mes in message:
            if mes.strip() == '':
                continue
            try:
                t, s = mes.strip().split("\t")
                t = t.strip()
                s = s.strip()
                s = s.lower()
                if s == 'battery_charged_on':
                    charged = True
                elif s == 'battery_charged_off':
                    charged = False
                elif s == 'wifi':
                    wifi = True
                elif s == 'unknown' or s == '4g' or s == '3g' or s == '2g':
                    wifi = False
                elif s == 'screen_on':
                    screen_off = False
                elif s == 'screen_off':
                    screen_off = True
                elif s == 'screen_lock':
                    locked = True
                elif s == 'screen_unlock':
                    locked = False
                elif s[-1] == '%':
                    battery_level = float(s[:-1])
                else:
                    print('invalid trace state: {}'.format(s))
                    idle = False # define: idle = locked
                    screen_off = False
                    locked = False 
                    wifi = False
                    charged = False
                    battery_level = 0.0
                    assert False
                
                # you can define your own 'idle' state
                idle = locked
                if idle and wifi and charged and st == None:
                    st = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - \
                         time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
                if (st != None) and not (idle and wifi and charged):
                    ed = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - \
                         time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
                    ready_time.append([st, ed])
                    st, ed = None, None
                
                if idle and charged and st_loose == None:
                    st_loose = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - \
                         time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
                if (st_loose != None) and not (idle and charged):
                    ed_loose = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - \
                         time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
                    ready_time_loose.append([st_loose, ed_loose])
                    st_loose, ed_loose = None, None
                
                
            except ValueError as e:
                # print('invalid trace for uid: {}'.format(self.ubt['guid']))
                # traceback.print_exc()
                assert False
                return

        # merge ready time
        try:
            ready_time = sorted(ready_time, key=lambda x: x[0])
            ready_time_loose = sorted(ready_time_loose, key=lambda x: x[0])
            now = ready_time[0]
            for a in ready_time:
                if now[1] >= a[0]:
                    now = [now[0], max(a[1], now[1])]
                else:
                    self.ready_time.append(now)
                    now = a
            self.ready_time.append(now)
            
            now = ready_time_loose[0]
            for a in ready_time_loose:
                if now[1] >= a[0]:
                    now = [now[0], max(a[1], now[1])]
                else:
                    self.ready_time_loose.append(now)
                    now = a
            self.ready_time_loose.append(now)
        except (ValueError, IndexError):
            # print('merge ready time error! invalid trace for uid: {}'.format(self.ubt['guid']))
            # traceback.print_exc()
            # assert False
            return

        # ### get trace start time and trace end time ###
        for mes in message:
            try:
                t = mes.strip().split("\t")[0].strip()
                if t == '':
                    continue
                sec = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - self.refer_second
                if not self.trace_start:
                    self.trace_start = sec
                self.trace_end = sec
            except ValueError:
                print('invalid trace for uid: {}'.format(self.ubt['guid']))
                # traceback.print_exc()
                # assert False
                return

        # print('user {} ready list: {}'.format(self.ubt['guid'], self.ready_time))
        self.isSuccess = True

    def ready(self, round_start, time_window, reference=True):
        """
        if client is ready at time: round_start + time_window
        :param round_start: round start time (reference time)
        :param time_window: execute time
        :param reference: if round_start a refer time or not
        :return: True if ready at round_start + time_window
        """
        if self.ubt == None:
            return True
        
        if not reference:
            round_start -= self.refer_second
        now = int(round_start + time_window - self.trace_start) % (int(self.trace_end - self.trace_start)) + self.trace_start
        for item in self.ready_time:
            if item[0] <= now <= item[1]:
                return True
        return False

    def get_available_time(self, time_start, time_window, reference=True):
        """
        get available time in [time_start, time_start + time_window]
        :param time_start: t
        :param time_window:  delta t
        :param reference: if round_start a refer time or not
        :return: time
        """

        if self.ubt == None:
            return sys.maxsize
        
        def overlay(S, E, t0, t1):
            # overlay of [S, E] and [t0, t1]
            res = 0
            if t0 <= S <= t1 <= E:
                res += t1 - S
            elif S <= t0 <= t1 <= E:
                res += t1 - t0
            elif S <= t0 <= E <= t1:
                res += E - t0
            elif t0 <= S <= E <= t1:
                res += E - S
            return res

        if not reference:
            time_start -= self.refer_second
        start = int(time_start - self.trace_start) % (int(self.trace_end - self.trace_start)) + self.trace_start
        end = start + time_window
        available_time = 0

        if end <= self.trace_end:
            for item in self.ready_time:
                available_time += overlay(start, end, item[0], item[1])
        else:
            trace_available = 0
            for item in self.ready_time:
                available_time += overlay(start, self.trace_end, item[0], item[1])
                end_ = int(end - self.trace_start) % (int(self.trace_end - self.trace_start)) + self.trace_start
                available_time += overlay(self.trace_start, end_, item[0], item[1])
                trace_available += item[1] - item[0]
            available_time += trace_available * (end - self.trace_end) // (self.trace_end - self.trace_start)
        return available_time
    
    def get_model(self):
        return self.model
    
    def get_avg_ready_time(self):
        res = 0
        if not self.isSuccess:
            return 0
        for item in self.ready_time:
            res += item[1] - item[0]
        return res/self.get_day()

    def get_avg_ready_time_loose(self):
        res = 0
        if not self.isSuccess:
            return 0
        for item in self.ready_time_loose:
            res += item[1] - item[0]
        return res/self.get_day()
    
    def get_day(self):
        return (self.trace_end - self.trace_start)/86400

class TraceHandler:
    def __init__(self):
        with open('normalized_guid2data.json', 'r', encoding='utf-8') as f:
            self.d = json.load(f)
        self.timers = []
    
    def get_tight_loose(self):
        # 获取在每个设备每天可以训练的平均时间
        model2time = {}
        model2time_loose = {}
        cnt = 0
        tot_ready_time = []
        tot_ready_time_loose = []
        for uid in self.d.keys():
            t = Timer(self.d[uid])
            self.timers.append(t)
            model = t.get_model()
            ready_time = t.get_avg_ready_time()
            ready_time_loose = t.get_avg_ready_time_loose()
            if model in model2time:
                model2time[model].append(ready_time)
            else:
                model2time[model] = [ready_time]
            if model in model2time_loose:
                model2time_loose[model].append(ready_time_loose)
            else:
                model2time_loose[model] = [ready_time_loose]
            cnt+=1
            if cnt%100 == 0:
                print('processed {} user traces'.format(cnt))
        print('user trace num: {}'.format(len(self.timers)))

        for model in model2time:
            lst = model2time[model]
            model2time[model] = sum(lst)/len(lst)
        for model in model2time_loose:
            lst = model2time_loose[model]
            model2time_loose[model] = sum(lst)/len(lst)
        
        with open('tight.json', 'w') as f:
            json.dump(model2time, f, indent = 2)
        with open('loose.json', 'w') as f:
            json.dump(model2time_loose, f, indent = 2)
    
    def get_model2cnt(self):
        self.du = Device_Util()
        # 获取每个机型对应的用户量
        model2cnt = defaultdict(int)
        with open('../raw_device_list.json', 'r') as f:
            raw_device_list = json.load(f)
        benchmark_models = [m['Model'] for m in raw_device_list]
        matched_models = set()
        for uid in self.d.keys():
            model = self.d[uid]['model']
            model2cnt[model] += 1
            if self.test_support(model):
                matched_models.add(model)
        with open('model2cnt.json', 'w') as f:
            json.dump(model2cnt, f, indent = 2)
        
        print('model num: {}'.format(len(model2cnt)))
        print('supported num: {}'.format(len(matched_models)))
        print('supported user: {}'.format(sum([model2cnt[model] for model in matched_models])))
        # print('matched model: {}'.format(matched_models))
        
        def cmp(x,y):
            return x > y
        
        sorted_model2cnt = sorted(model2cnt.items(), key=lambda x: x[1], reverse = True)
        sorted_model2cnt_dict = {item[0]:item[1] for item in sorted_model2cnt}
        unsupported_model = sorted_model2cnt_dict
        
        for model in matched_models:
            unsupported_model.pop(model)
        with open('unsupported_model.json', 'w') as f:
            json.dump(unsupported_model, f, indent = 2)

        with open('sorted_model2cnt.json', 'w') as f:
            json.dump(sorted_model2cnt_dict, f, indent = 2)
        
        # print(sorted_model2cnt[:200])

        cnt_list = [item[1] for item in sorted_model2cnt]
        cdf = [cnt_list[0]]
        for i in range(1, len(cnt_list)):
            cdf.append(cdf[i-1] + cnt_list[i])
        print(cdf[-5:])
        perc = cdf[-1]*0.95
        print('perc: {}'.format(perc))
        flag = False
        while not flag:
            try:
                ii = cdf.index(int(perc))
                flag = True
            except Exception as e:
                perc += 1
        
        print('iter: {}'.format(ii))
        
    def test_support(self, model):
        return self.du.is_support(model)
    
    def test_support_tight(self, model):
        return self.du.is_support_tight(model)

    def test_transfer(self):
        self.du = Device_Util()
        supported2cnt = defaultdict(int)
        tight_supported2cnt = defaultdict(int)
        transfer = {}
        with open('model2cnt.json','r') as f:
            model2cnt = json.load(f)
        for model in model2cnt:
            transfered_model = self.du.transfer(model)
            # print('real model ({}) is transfered to ({})'.format(model, transfered_model))
            transfer[model] = transfered_model
            supported2cnt[transfered_model] += model2cnt[model]
            if self.test_support_tight(model):
                tight_supported2cnt[transfered_model] += model2cnt[model]
        with open('tight_supported2cnt.json', 'w') as f:
            json.dump(tight_supported2cnt, f, indent=2)
        with open('supported2cnt.json', 'w') as f:
            json.dump(supported2cnt, f, indent=2)
        with open('transfer.json', 'w') as f:
            json.dump(transfer, f, indent=2)
    

if __name__ == "__main__":
    th = TraceHandler()
    th.get_model2cnt()
    th.test_transfer()
