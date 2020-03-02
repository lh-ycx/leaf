import json
import os
import time
from datetime import datetime


class Timer:
    def __init__(self, ubt, google=True):
        self.isSuccess = False
        self.fmt = '%Y-%m-%d %H:%M:%S'
        self.refer_time = '2020-01-02 00:00:00'
        self.refer_second = time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
        self.trace_start, self.trace_end = None, None
        self.setting = [[], [], [], [], []]
        self.google = google
        self.model = ubt['model']
        self.state = ['battery_charged_off', 'battery_charged_on', 'battery_low', 'battery_okay',
                      'phone_off', 'phone_on', 'screen_off', 'screen_on', 'screen_unlock']

        # get marched ubt from user_behavior_tiny by uid
        self.ubt = ubt

        if ubt is None:  # no user trace will be used
            self.isSuccess = True
            return

        # ### get ready time list ###
        message = self.ubt['messages'].split('\n')
        idle = False  # define: idle = locked
        screen_off = False
        locked = False
        wifi = False
        charged = False
        battery_level = 0.0
        st = [None, None, None, None, None]
        ed = [None, None, None, None, None]
        for mes in message:
            # print(mes)
            if mes.strip() == '':
                continue
            try:
                t, s = mes.strip().split("\t")
                t = t.strip()
                s = s.strip().lower()
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
                    idle = False  # define: idle = locked
                    screen_off = False
                    locked = False
                    wifi = False
                    charged = False
                    battery_level = 0.0
                    assert False

                # you can define your own 'idle' state
                idle = locked
                ok = [
                    None,
                    (idle and wifi and charged),
                    (idle and charged),
                    (idle and wifi and (battery_level >= 50.0 or charged)),
                    (idle and (battery_level >= 50.0 or charged))
                ]

                for i in range(1, 5):
                    if ok[i] and st[i] is None:
                        st[i] = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - \
                                time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
                    elif (st[i] is not None) and not ok[i]:
                        ed[i] = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - \
                                time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
                        self.setting[i].append([st[i], ed[i]])
                        st[i], ed[i] = None, None

                # print(self.setting)
                # print()

            except ValueError as e:
                # print('invalid trace for uid: {}'.format(self.ubt['guid']))
                # traceback.print_exc()
                assert False

        # merge ready time
        try:
            for i in range(1, 5):
                ready_time = sorted(self.setting[i], key=lambda x: x[0])
                self.setting[i] = []
                now = ready_time[0]
                for a in ready_time:
                    if now[1] >= a[0]:
                        now = [now[0], max(a[1], now[1])]
                    else:
                        self.setting[i].append(now)
                        now = a
                self.setting[i].append(now)

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

    def get_avg_ready_time(self, setting=1):
        res = 0
        if not self.isSuccess:
            return 0
        for item in self.setting[setting]:
            res += item[1] - item[0]
        return res / self.get_day()

    def get_day(self):
        return (self.trace_end - self.trace_start) / 86400


if __name__ == '__main__':
    input_dir = 'data'
    with open(os.path.join(input_dir, 'normalized_guid2data.json'), 'r') as f:
        guid2data = json.load(f)
    for key in guid2data:
        timer = Timer(guid2data[key])
        for i in range(1, 5):
            print(timer.get_avg_ready_time(i), timer.setting[i])
        print()
