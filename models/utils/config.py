import os
from .logger import Logger
import traceback

L = Logger()
logger = L.get_logger()

DEFAULT_CONFIG_FILE = 'default.cfg'

# configuration for FedAvg
class Config():
    def __init__(self, config_file = 'default.cfg'):
        self.dataset = 'shakespeare'
        self.model = 'stacked_lstm'
        self.num_rounds = -1            # -1 for unlimited
        self.lr = 0.1
        self.eval_every = 3             # -1 for eval when quit
        self.clients_per_round = 10
        self.batch_size = 10
        self.seed = 0
        self.metrics_file = 'metrics'
        self.num_epochs = 1
        self.gpu_fraction = 0.2
        self.minibatch = None       # always None for FedAvg
        self.round_ddl = [1000, 0]
        self.update_frac = 0.5
        self.big_upload_time = [5.0, 1.0]
        self.mid_upload_time = [10.0, 1.0]
        self.small_upload_time = [15.0, 1.0]
        self.big_speed = [150.0, 1.0]
        self.mid_speed = [100.0, 1.0]
        self.small_speed = [50.0, 1.0]
        
        logger.info('read config from {}'.format(config_file))
        self.read_config(config_file)
        self.log_config()
        
        
    def read_config(self, filename = DEFAULT_CONFIG_FILE):
        if not os.path.exists(filename):
            logger.error('ERROR: config file {} does not exist!'.format(filename))
            assert False
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                try:
                    line = line.split()
                    if line[0] == 'num_rounds':
                        self.num_rounds = int(line[1])
                    elif line[0] == 'learning_rate':
                        self.lr = float(line[1])
                    elif line[0] == 'eval_every':
                        self.eval_every = int(line[1])
                    elif line[0] == 'clients_per_round':
                        self.clients_per_round = int(line[1])
                    elif line[0] == 'batch_size':
                        self.batch_size = int(line[1])
                    elif line[0] == 'seed':
                        self.seed = int(line[1])
                    elif line[0] == 'metrics_file':
                        self.metrics_file = str(line[1])
                    elif line[0] == 'num_epochs':
                        self.num_epochs = int(line[1])
                    elif line[0] == 'dataset':
                        self.dataset = str(line[1])
                    elif line[0] == 'model':
                        self.model = str(line[1])
                    elif line[0] == 'gpu_fraction':
                        self.gpu_fraction = float(line[1])
                    elif line[0] == 'round_ddl':
                        self.round_ddl = [float(line[1]), float(line[2])]
                    elif line[0] == 'update_frac':
                        self.update_frac = float(line[1])
                    elif line[0] == 'big_upload_time':
                        self.big_upload_time = [float(line[1]), float(line[2])]
                    elif line[0] == 'mid_upload_time':
                        self.mid_upload_time = [float(line[1]), float(line[2])]
                    elif line[0] == 'small_upload_time':
                        self.small_upload_time = [float(line[1]), float(line[2])]
                    elif line[0] == 'big_speed':
                        self.big_speed = [float(line[1]), float(line[2])]
                    elif line[0] == 'mid_speed':
                        self.mid_speed = [float(line[1]), float(line[2])]
                    elif line[0] == 'small_speed':
                        self.small_speed = [float(line[1]), float(line[2])]
                except Exception as e:
                    traceback.print_exc()
    
    def log_config(self):
        configs = vars(self)
        logger.info('================= Config =================')
        for key in configs.keys():
            logger.info('\t{} = {}'.format(key, configs[key]))
        logger.info('================= ====== =================')
        
