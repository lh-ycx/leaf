## TODO use rank instead of the score to find the nearest model
## TODO change small middle big device to our real wupported device


import json
import traceback
import sys
import os
cur_dir = os.path.dirname(__file__)

class Device_Util:
    
    def __init__(self):
        try:
            with open(os.path.join(cur_dir, 'real2benchmark.json')) as f:
                self.real2benchmark = json.load(f)
            with open(os.path.join(cur_dir, 'benchmark2score.json')) as f:
                self.benchmark2score = json.load(f)
            with open(os.path.join(cur_dir, 'supported_devices.json')) as f:
                self.supported_devices = json.load(f)
                self.supported_score = [self.benchmark2score[device] for device in self.supported_devices]
                self.supported_rank = [list(self.benchmark2score).index(device) for device in self.supported_devices]
                # print('supported_score: {}'.format(self.supported_score))
                # print('supported_rank: {}'.format(self.supported_rank))

        except Exception as e:
            traceback.print_exc()
            print('need real2benchmark.json, benchmark2score.json, and supported_devices.json')
            raise e
    
    def transfer(self, real_device):
        '''
            transfer device from the real-world trace to the nearest supported device
            Args:
                real_device: device model from the real-world trace
            Return:
                transfered_device: nearest supported device model
        '''
        try:
            if real_device in self.real2benchmark:
                benchmark_device = self.real2benchmark[real_device]
                if "unknown" in benchmark_device:
                    return self.unknown()
                '''
                # old implementation - use rank
                benchmark_devices = list(self.benchmark2score)
                rank = benchmark_devices.index(benchmark_device)
                min_delta = sys.maxsize
                min_iter = 0
                for i in range(len(self.supported_devices)):
                    delta = abs(rank - self.supported_rank[i])
                    if delta < min_delta:
                        min_delta = delta
                        min_iter = i
                '''
                
                score = self.benchmark2score[benchmark_device]
                _min_delta = sys.maxsize
                _min_iter = 0
                for i in range(len(self.supported_devices)):
                    delta = abs(score - self.supported_score[i])
                    if delta < _min_delta:
                        _min_delta = delta
                        _min_iter = i
                
                # if _min_iter != min_iter:
                    # print('find {} --- min_iter:{}, _min_iter:{}'.format(real_device, min_iter, _min_iter))
                
                return self.supported_devices[_min_iter]
            return self.unknown()
        except Exception as e:
            # traceback.print_exc()
            return self.unknown()
    

    def unknown(self):
        '''
            return the default supported device model
            Args:
                None
            Return:
                default supported device model
        '''
        return self.supported_devices[1]
    
    def is_support(self, real_device):
        '''
            return if device is suported under our implementation(it can be unknown)
            Args:
                real_device: device model from the trace (need to be transfered because they have
                    different model naming patterns)
            Return:
                res: True for support and vice versa
        '''
        return real_device in self.real2benchmark
    
    def is_support_tight(self, real_device):
        '''
            return if device is suported in ai benchmark(unknown is not supported in this case)
            Args:
                real_device: device model from the trace (need to be transfered because they have
                    different model naming patterns)
            Return:
                res: True for support and vice versa
        '''
        return real_device in self.real2benchmark and 'unknown' not in self.real2benchmark[real_device]
    
    def get_train_time(self, model, num_sample, batch_size, num_epoch):
        '''
            return the training time using look up table
            Args:
                model: device model(should be supported)
                num_sample: number of samples
                batch_size: batch size
                num_epoch: number of epoches
        '''

        # TODO - finish look up table
        reddit_profile_data = [6.5, 4.1, 1.5]
        ii = self.supported_devices.index(model)
        return num_epoch * ((num_sample-1)//batch_size + 1) * reddit_profile_data[ii]


if __name__ == "__main__":
    du = Device_Util()
    du.transfer('motorola one vision')