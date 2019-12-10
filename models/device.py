# simulate device type
# current classify as big/middle/small device
# device can also be 
from utils.logger import Logger
import numpy as np

# -1 - self define device, 0 - small, 1 - mid, 2 - big
support_device = ['small_device', 'mid_device', 'big_device']

L = Logger()
logger = L.get_logger()

class Device():
    
    # self defined device
    def __init__(self, upload_time_u, upload_time_sigma, speed_u, speed_sigma, device_name):
        self.device_type = -1   # self defined device
        self.device_name = device_name
        
        self.upload_time_u = upload_time_u
        self.upload_time_sigma = upload_time_sigma
        self.speed_u = speed_u
        self.speed_sigma = speed_sigma
        
    # support device type
    def __init__(self, device_type, cfg):
        if device_type >= len(support_device):
            logger.error('invalid device type!')
            assert False
        self.device_type = device_type
        self.device_name = support_device[device_type]
        
        if device_type == 0:
            self.upload_time_u = cfg.small_upload_time[0]
            self.upload_time_sigma = cfg.small_upload_time[1]
            self.speed_u = cfg.small_speed[0]
            self.speed_sigma = cfg.small_speed[1]
        elif device_type == 1:
            self.upload_time_u = cfg.mid_upload_time[0]
            self.upload_time_sigma = cfg.mid_upload_time[1]
            self.speed_u = cfg.mid_speed[0]
            self.speed_sigma = cfg.mid_speed[1]
        elif device_type == 2:
            self.upload_time_u = cfg.big_upload_time[0]
            self.upload_time_sigma = cfg.big_upload_time[1]
            self.speed_u = cfg.big_speed[0]
            self.speed_sigma = cfg.big_speed[1]
        else:
            logger.error('???')
            assert False
    
    def get_speed(self):
        speed = np.random.normal(self.speed_u, self.speed_sigma)
        while speed <= 0:
            speed = np.random.normal(self.speed_u, self.speed_sigma)
        return int(speed)
    
    def get_upload_time(self):
        upload_time = np.random.normal(self.upload_time_u, self.upload_time_sigma)
        while upload_time <= 0:
            upload_time = np.random.normal(self.upload_time_u, self.upload_time_sigma)
        return int(upload_time)
    
