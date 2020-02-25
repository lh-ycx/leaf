# simulate device type
# current classify as big/middle/small device
# device can also be 
from utils.logger import Logger
from utils.device_util.device_util import Device_Util
import numpy as np

# -1 - self define device, 0 - small, 1 - mid, 2 - big

L = Logger()
logger = L.get_logger()

class Device():
        
    du = Device_Util()

    # support device type
    def __init__(self, cfg):
        self.device_model = None    # later set according to the trace
        self.upload_time_u = cfg.upload_time[0]
        self.upload_time_sigma = cfg.upload_time[1]
        
        Device.du.set_model(cfg.model)
        Device.du.set_dataset(cfg.dataset)

    def set_device_model(self, real_device_model):
        self.device_model = Device.du.transfer(real_device_model)

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
        return Device.du.get_train_time(self.device_model, num_sample, batch_size, num_epoch)
        