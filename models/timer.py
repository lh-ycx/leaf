import json
import time
from datetime import datetime
import random
import pandas as pd
import traceback
from utils.logger import Logger

L = Logger()
logger = L.get_logger()


class Timer:
    def __init__(self, ubt, google=True):
        self.isSuccess = False
        self.fmt = '%Y-%m-%d %H:%M:%S'
        self.refer_time = '2020-01-02 00:00:00'
        self.refer_second = time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
        self.trace_start, self.trace_end = None, None
        self.ready_time = []
        self.google = google
        self.state = ['battery_charged_off', 'battery_charged_on', 'battery_low', 'battery_okay',
                      'phone_off', 'phone_on', 'screen_off', 'screen_on', 'screen_unlock']

        # get marched ubt from user_behavior_tiny by uid
        self.ubt = ubt

        # ### get ready time list ###
        start_charge, end_charge, okay, low = None, None, None, None
        message = self.ubt['messages'].split('\n')
        ready_time = []
        # for s in self.state:
            # message = message.replace(s, "\t" + s + "\n")
        # message = message.replace('\x00', '').strip().split("\n")
        # get ready time
        
        idle = False # define: idle = locked
        screen_off = False
        locked = False 
        wifi = False
        charged = False
        battery_level = 0.0
        st = None   # ready start time
        ed = None   # ready end time
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
                    logger.error('invalid trace state: {}'.format(s))
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
                
                '''
                if s == 'battery_charged_on' and not start_charge:
                    start_charge = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - \
                                   time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
                elif s == 'battery_charged_off' and start_charge:
                    end_charge = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - \
                                 time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
                    ready_time.append([start_charge, end_charge])
                    start_charge, end_charge = None, None

                if not self.google:
                    if s == 'battery_okay' and not okay:
                        okay = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - \
                               time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
                    elif s == 'battery_low' and okay:
                        low = time.mktime(datetime.strptime(t, self.fmt).timetuple()) - \
                              time.mktime(datetime.strptime(self.refer_time, self.fmt).timetuple())
                        ready_time.append([okay, low])
                        okay, low = None, None
                '''
            except ValueError as e:
                logger.debug('invalid trace for uid: {}'.format(self.ubt['guid']))
                # traceback.print_exc()
                # assert False
                return

        # merge ready time
        try:
            ready_time = sorted(ready_time, key=lambda x: x[0])
            now = ready_time[0]
            for a in ready_time:
                if now[1] >= a[0]:
                    now = [now[0], max(a[1], now[1])]
                else:
                    self.ready_time.append(now)
                    now = a
            self.ready_time.append(now)
        except (ValueError, IndexError):
            logger.debug('merge ready time error! invalid trace for uid: {}'.format(self.ubt['guid']))
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
                logger.debug('invalid trace for uid: {}'.format(self.ubt['guid']))
                # traceback.print_exc()
                # assert False
                return

        logger.debug('usr {} ready list: {}'.format(self.ubt['guid'], self.ready_time))
        self.isSuccess = True

    def ready(self, round_start, time_window, reference=True):
        """
        if client is ready at time: round_start + time_window
        :param round_start: round start time (reference time)
        :param time_window: execute time
        :param reference: if round_start a refer time or not
        :return: True if ready at round_start + time_window
        """
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