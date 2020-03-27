import random
import warnings
import timeout_decorator
import sys
import numpy as np
import json

from utils.logger import Logger
from device import Device
from timer import Timer

L = Logger()
logger = L.get_logger()

class Client:
    
    d = None
    try:
        with open('/home/ubuntu/storage/ycx/feb_trace/normalized_guid2data.json', 'r', encoding='utf-8') as f:
            d = json.load(f)
    except FileNotFoundError as e:
        d = None
        logger.warn('no user behavior trace was found, running in no-trace mode')
    
    def __init__(self, client_id, group=None, train_data={'x' : [],'y' : []}, eval_data={'x' : [],'y' : []}, model=None, device=None, cfg=None):
        self._model = model
        self.id = client_id # integer
        self.group = group
        self.train_data = train_data
        self.eval_data = eval_data
        self.deadline = 1 # < 0 for unlimited
        self.cfg = cfg
        
        self.device = device  # if device == none, it will use real time as train time and set upload time as 0
        if self.device == None:
            logger.warn('client {} with no device init, upload time will be set as 0 and speed will be the gpu spped'.format(self.id))
            self.upload_time = 0
        
        # timer
        d = Client.d
        if d == None:
            cfg.user_trace = False
        # uid = random.randint(0, len(d))
        if cfg.user_trace and cfg.real_world == False:
            uid = random.sample(list(d.keys()), 1)[0]
            self.timer = Timer(ubt=d[str(uid)], google=True)
            while self.timer.isSuccess != True:
                uid = random.sample(list(d.keys()), 1)[0]
                self.timer = Timer(ubt=d[str(uid)], google=True)
        elif cfg.user_trace and cfg.real_world == True:
            uid = self.id
            self.timer = Timer(ubt=d[str(uid)], google=True)
        else:
            self.timer = Timer(None)
            self.deadline = sys.maxsize # deadline is meaningless without user trace
        
        real_device_model = self.timer.model
        if self.device is not None:
            self.device.set_device_model(real_device_model)


    def train(self, start_t=None, num_epochs=1, batch_size=10, minibatch=None):
        """Trains on self.model using the client's train_data.

        Args:
            num_epochs: Number of epochs to train. Unsupported if minibatch is provided (minibatch has only 1 epoch)
            batch_size: Size of training batches.
            minibatch: fraction of client's data to apply minibatch sgd,
                None to use FedAvg
            start_t: strat time of the training, only used in train_with_simulate_time
        Return:
            comp: number of FLOPs executed in training process
            num_samples: number of samples used in training
            update: set of weights
            update_size: number of bytes in update
        """
        
        train_time_limit = self.get_train_time_limit()
        logger.debug('train_time_limit: {}'.format(train_time_limit))
        
        def train_with_simulate_time(self, start_t, num_epochs=1, batch_size=10, minibatch=None):
            if minibatch is None:
                num_data = min(len(self.train_data["x"]), self.cfg.max_sample)
            else :
                frac = min(1.0, minibatch)
                num_data = max(1, int(frac*len(self.train_data["x"])))
            
            # train_speed = self.device.get_speed()
            # train_time = (len(self.train_data['y'])*num_epochs)/train_speed
            # TODO finish device - use a regression model to predict the training time
            logger.debug('client {}: num data:{}'.format(self.id, num_data))
            train_time = self.device.get_train_time(num_data, batch_size, num_epochs) # num_sample, batch_size, num_epoch
            upload_time = self.deadline - train_time_limit
            available_time = self.timer.get_available_time(start_t, train_time_limit)
            logger.debug('client {}: train time:{}'.format(self.id, train_time))
            logger.debug('client {}: available time:{}'.format(self.id, available_time))
            
            # compute num_data
            if minibatch is None:
                num_data = min(len(self.train_data["x"]), self.cfg.max_sample)
                xs, ys = zip(*random.sample(list(zip(self.train_data["x"], self.train_data["y"])), num_data))
                data = {'x': xs, 'y': ys}
            else:
                frac = min(1.0, minibatch)
                num_data = max(1, int(frac*len(self.train_data["x"])))
                xs, ys = zip(*random.sample(list(zip(self.train_data["x"], self.train_data["y"])), num_data))
                data = {'x': xs, 'y': ys}
            
            if train_time > train_time_limit:
                # data sampling
                comp = self.model.get_comp(data, num_epochs, batch_size)
                self.actual_comp = int(comp*train_time_limit/train_time)    # will be used in get_actual_comp
                failed_reason = 'data sampling: train_time({}) + upload_time({}) > deadline({})'.format(train_time, upload_time, self.deadline)
                raise timeout_decorator.timeout_decorator.TimeoutError(failed_reason)
            elif train_time > available_time:
                # client interruption
                comp = self.model.get_comp(data, num_epochs, batch_size)
                self.actual_comp = int(comp*train_time_limit/train_time)    # will be used in get_actual_comp
                failed_reason = 'client interruption: train_time({}) > available_time({})'.format(train_time, available_time)
                raise timeout_decorator.timeout_decorator.TimeoutError(failed_reason)
            else :
                if minibatch is None:
                    if self.cfg.no_training:
                        comp = self.model.get_comp(data, num_epochs, batch_size)
                        update, acc, loss = -1,-1,-1
                    else:
                        comp, update, acc, loss = self.model.train(data, num_epochs, batch_size)
                else:
                    # Minibatch trains for only 1 epoch - multiple local epochs don't make sense!
                    num_epochs = 1
                    if self.cfg.no_training:
                        comp = self.model.get_comp(data, num_epochs, num_data)
                        update, acc, loss = -1,-1,-1
                    else:
                        comp, update, acc, loss = self.model.train(data, num_epochs, num_data)
                num_train_samples = len(data['y'])
                simulate_time_c = train_time + self.upload_time
                self.actual_comp = comp
                return simulate_time_c, comp, num_train_samples, update, acc, loss
        
        @timeout_decorator.timeout(train_time_limit)
        def train_with_real_time_limit(self, num_epochs=1, batch_size=10, minibatch=None):
            start_time = time.time()
            if minibatch is None:
                # data = self.train_data
                num_data = min(len(self.train_data["x"]), self.cfg.max_sample)
                xs, ys = zip(*random.sample(list(zip(self.train_data["x"], self.train_data["y"])), num_data))
                data = {'x': xs, 'y': ys}
                if self.cfg.no_training:
                    comp, update, acc, loss = -1,-1,-1,-1
                else:
                    comp, update, acc, loss = self.model.train(data, num_epochs, batch_size)
            else:
                frac = min(1.0, minibatch)
                num_data = max(1, int(frac*len(self.train_data["x"])))
                xs, ys = zip(*random.sample(list(zip(self.train_data["x"], self.train_data["y"])), num_data))
                data = {'x': xs, 'y': ys}

                # Minibatch trains for only 1 epoch - multiple local epochs don't make sense!
                num_epochs = 1
                if self.cfg.no_training:
                    comp, update, acc, loss = -1,-1,-1,-1
                else:
                    comp, update, acc, loss = self.model.train(data, num_epochs, num_data)
            num_train_samples = len(data['y'])
            simulate_time_c = time.time() - start_time
            return simulate_time_c, comp, num_train_samples, update, acc, loss
        
        if self.device == None:
            return train_with_real_time_limit(self, num_epochs, batch_size, minibatch)
        else:
            return train_with_simulate_time(self, start_t, num_epochs, batch_size, minibatch)

    def test(self, set_to_use='test'):
        """Tests self.model on self.test_data.
        
        Args:
            set_to_use. Set to test on. Should be in ['train', 'test'].
        Return:
            dict of metrics returned by the model.
        """
        assert set_to_use in ['train', 'test', 'val']
        if set_to_use == 'train':
            data = self.train_data
        elif set_to_use == 'test' or set_to_use == 'val':
            data = self.eval_data
        return self.model.test(data)

    @property
    def num_test_samples(self):
        """Number of test samples for this client.

        Return:
            int: Number of test samples for this client
        """
        if self.eval_data is None:
            return 0
        return len(self.eval_data['y'])

    @property
    def num_train_samples(self):
        """Number of train samples for this client.

        Return:
            int: Number of train samples for this client
        """
        if self.train_data is None:
            return 0
        return len(self.train_data['y'])

    @property
    def num_samples(self):
        """Number samples for this client.

        Return:
            int: Number of samples for this client
        """
        train_size = 0
        if self.train_data is not None:
            train_size = len(self.train_data['y'])

        test_size = 0 
        if self.eval_data is not  None:
            test_size = len(self.eval_data['y'])
        return train_size + test_size

    @property
    def model(self):
        """Returns this client reference to model being trained"""
        return self._model

    @model.setter
    def model(self, model):
        warnings.warn('The current implementation shares the model among all clients.'
                      'Setting it on one client will effectively modify all clients.')
        self._model = model
    
    
    def set_deadline(self, deadline = -1):
        if deadline < 0 or not self.cfg.user_trace:
            self.deadline = sys.maxsize
        else:
            self.deadline = deadline
        logger.debug('client {}\'s deadline is set to {}'.format(self.id, self.deadline))
    
    def set_upload_time(self, upload_time):
        if upload_time > 0:
            self.upload_time = upload_time
        else:
            logger.error('invalid upload time: {}'.format(upload_time))
            assert False
        logger.debug('client {}\'s upload_time is set to {}'.format(self.id, self.upload_time))
    
    def get_train_time_limit(self):
        if self.device != None:
            self.upload_time = self.device.get_upload_time()
            logger.debug('client {} upload time: {}'.format(self.id, self.upload_time))
        if self.upload_time < self.deadline :
            # logger.info('deadline: {}'.format(self.deadline))
            return self.deadline - self.upload_time
        else:
            return 0.01
    

    def upload_suc(self, start_t, num_epochs=1, batch_size=10, minibatch=None):
        """Test if this client will upload successfully

        Args:
            num_epochs: Number of epochs to train. Unsupported if minibatch is provided (minibatch has only 1 epoch)
            batch_size: Size of training batches.
            minibatch: fraction of client's data to apply minibatch sgd,
                None to use FedAvg
            start_t: strat time of the training, only used in train_with_simulate_time
        Return:
            result: test result(True or False)
        """
        train_time_limit = self.get_train_time_limit()
        logger.debug('train_time_limit: {}'.format(train_time_limit))
        if minibatch is None:
            num_data = min(len(self.train_data["x"]), self.cfg.max_sample)
        else :
            frac = min(1.0, minibatch)
            num_data = max(1, int(frac*len(self.train_data["x"])))
        
        train_time = self.device.get_train_time(num_data, batch_size, num_epochs) # num_sample, batch_size, num_epoch
        upload_time = self.deadline - train_time_limit
        available_time = self.timer.get_available_time(start_t, train_time_limit)
        logger.debug('client {}: train time:{}'.format(self.id, train_time))
        logger.debug('client {} available time:{}'.format(self.id, available_time))
        if train_time > train_time_limit:
            return False
        elif train_time > available_time:
            return False
        else:
            return True

    
    def get_device_model(self):
        if self.device == None:
            return 'None'
        return self.device.device_model
        
    def get_actual_comp(self):
        '''
        get the actual computation in the training process
        '''
        return self.actual_comp
