# simulate device type
# current classify as big/middle/small device
# device can also be 
from utils.logger import Logger
from utils.device_util.device_util import Device_Util
import numpy as np

# -1 - self define device, 0 - small, 1 - mid, 2 - big
du = Device_Util()

L = Logger()
logger = L.get_logger()

class Device():
        
    # support device type
    def __init__(self, cfg):
        self.device_model = None    # later set according to the trace
        self.upload_time_u = cfg.upload_time[0]
        self.upload_time_sigma = cfg.upload_time[1]
        
        '''
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
        '''
    
    '''
    def get_speed(self):
        speed = np.random.normal(self.speed_u, self.speed_sigma)
        while speed < 0:
            speed = np.random.normal(self.speed_u, self.speed_sigma)
        return float(speed)
    '''
    
    def set_device_model(self, real_device_model):
        self.device_model = du.transfer(real_device_model)

    def get_upload_time(self):
        upload_time = np.random.normal(self.upload_time_u, self.upload_time_sigma)
        while upload_time < 0:
            upload_time = np.random.normal(self.upload_time_u, self.upload_time_sigma)
        return float(upload_time)
    
    def get_train_time(self, num_sample, batch_size, num_epoch):
        # TODO - finish train time predictor

        # current implementation: 
        # use real data withour prediction, 
        # so now it does not support other models
        if self.device_model == None:
            assert False
        return du.get_train_time(self.device_model, num_sample, batch_size, num_epoch)
        