"""Script to run the baselines."""
import argparse
import importlib
import numpy as np
import os
import sys
import random
import time
import eventlet
import signal
import tensorflow as tf

import metrics.writer as metrics_writer

config_name = 'reddit_FedAvg_1'     # dataset_aggregateAlgorithm_E
    
# logger
from utils.logger import Logger
L = Logger()
L.set_log_name(config_name)
logger = L.get_logger()

from baseline_constants import MAIN_PARAMS, MODEL_PARAMS
from client import Client
from server import Server
from model import ServerModel

from utils.args import parse_args
from utils.model_utils import read_data
from utils.config import Config
from device import Device

STAT_METRICS_PATH = 'metrics/stat_metrics.csv'
SYS_METRICS_PATH = 'metrics/sys_metrics.csv'

def main():
    eventlet.monkey_patch()
    args = parse_args()
    
    '''
    config_name = args.config_file
    while config_name[-4:] == '.cfg':
        config_name = config_name[:-4]
    '''
    
    # read config from file
    cfg = Config('{}.cfg'.format(config_name))

    # Set the random seed if provided (affects client sampling, and batching)
    random.seed(1 + cfg.seed)
    np.random.seed(12 + cfg.seed)
    tf.compat.v1.set_random_seed(123 + cfg.seed)

    model_path = '%s/%s.py' % (cfg.dataset, cfg.model)
    if not os.path.exists(model_path):
        logger.error('Please specify a valid dataset and a valid model.')
        assert False
    model_path = '%s.%s' % (cfg.dataset, cfg.model)
    
    logger.info('############################## %s ##############################' % model_path)
    mod = importlib.import_module(model_path)
    ClientModel = getattr(mod, 'ClientModel')

    '''
    tup = MAIN_PARAMS[args.dataset][args.t]
    num_rounds = args.num_rounds if args.num_rounds != -1 else tup[0]
    eval_every = args.eval_every if args.eval_every != -1 else tup[1]
    clients_per_round = args.clients_per_round if args.clients_per_round != -1 else tup[2]
    '''
    
    num_rounds = cfg.num_rounds
    eval_every = cfg.eval_every
    clients_per_round = cfg.clients_per_round
    
    # Suppress tf warnings
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    # Create 2 models
    model_params = MODEL_PARAMS[model_path]
    if cfg.lr != -1:
        model_params_list = list(model_params)
        model_params_list[0] = cfg.lr
        model_params = tuple(model_params_list)

    # Create client model, and share params with server model
    tf.reset_default_graph()
    client_model = ClientModel(cfg.seed, *model_params, cfg.gpu_fraction)

    # Create clients
    clients = setup_clients(cfg, client_model)
    # print(sorted([c.num_train_samples for c in clients]))
    # Create server
    server = Server(client_model, clients, cfg = cfg)
    
    client_ids, client_groups, client_num_samples = server.get_clients_info(clients)
    
    logger.info('Clients in Total: %d' % (len(clients)))

    # Initial status
    logger.info('===================== Random Initialization =====================')
    stat_writer_fn = get_stat_writer_function(client_ids, client_groups, client_num_samples, args)
    sys_writer_fn = get_sys_writer_function(args)
    # print_stats(0, server, clients, client_num_samples, args, stat_writer_fn)

    # Simulate training
    if num_rounds == -1:
        import sys
        num_rounds = sys.maxsize
        
    def timeout_handler(signum, frame):
        raise Exception
    
    def exit_handler(signum, frame):
        os._exit(0)
    
    for i in range(num_rounds):
        round_start_time = time.time()
        logger.info('===================== Round {} of {} ====================='.format(i+1, num_rounds))
        
        # 1. selection stage
        logger.info('--------------------- selection stage ---------------------')
        # 1.1 select clients
        server.select_clients(i, online(clients), num_clients=clients_per_round)
        c_ids, c_groups, c_num_samples = server.get_clients_info(server.selected_clients)
        logger.info("selected client_ids: {}".format(c_ids))
        # 1.2 decide deadline for each client
        deadline = np.random.normal(cfg.round_ddl[0], cfg.round_ddl[1])
        while deadline <= 0:
            deadline = np.random.normal(cfg.round_ddl[0], cfg.round_ddl[1])
        deadline = int(deadline)
        logger.info('selected deadline: {}'.format(deadline))
        
        # 2. configuration stage
        logger.info('--------------------- configuration stage ---------------------')
        # 2.1 train(no parallel implementation)
        sys_metrics = server.train_model(num_epochs=cfg.num_epochs, batch_size=cfg.batch_size, minibatch=cfg.minibatch, deadline = deadline)
        sys_writer_fn(i + 1, c_ids, sys_metrics, c_groups, c_num_samples)
        
        # 3. update stage
        logger.info('--------------------- report stage ---------------------')
        # 3.1 update global model
        server.update_model(cfg.update_frac)
        
        # 3.2 total simulation time for this round
        logger.info("simulating round {} used {} seconds".format(i+1, time.time()-round_start_time))
        
        # 4. Test model(if necessary)
        if eval_every == -1:
            continue
        if (i + 1) % eval_every == 0 or (i + 1) == num_rounds:
            logger.info('--------------------- test result ---------------------')
            test_clients = random.sample(clients, 50)
            sc_ids, sc_groups, sc_num_samples = server.get_clients_info(test_clients)
            logger.info('number of clients for test: {} of {} '.format(len(test_clients),len(clients)))
            another_stat_writer_fn = get_stat_writer_function(sc_ids, sc_groups, sc_num_samples, args)
            # print_stats(i + 1, server, test_clients, client_num_samples, args, stat_writer_fn)
            print_stats(i + 1, server, test_clients, sc_num_samples, args, another_stat_writer_fn)
    
    # Save server model
    ckpt_path = os.path.join('checkpoints', cfg.dataset)
    if not os.path.exists(ckpt_path):
        os.makedirs(ckpt_path)
    save_path = server.save_model(os.path.join(ckpt_path, '{}.ckpt'.format(cfg.model)))
    logger.info('Model saved in path: %s' % save_path)

    # Close models
    server.close_model()

def online(clients):
    """We assume all users are always online."""
    return clients


def create_clients(users, groups, train_data, test_data, model, cfg):
    if len(groups) == 0:
        groups = [[] for _ in users]
    # clients = [Client(u, g, train_data[u], test_data[u], model, random.randint(0, 2), cfg) for u, g in zip(users, groups)]
    clients = [Client(u, g, train_data[u], test_data[u], model, Device(random.randint(0, 2), cfg)) for u, g in zip(users, groups)]
    return clients


def setup_clients(cfg, model=None, use_val_set=False):
    """Instantiates clients based on given train and test data directories.

    Return:
        all_clients: list of Client objects.
    """
    eval_set = 'test' if not use_val_set else 'val'
    train_data_dir = os.path.join('..', 'data', cfg.dataset, 'data', 'train')
    test_data_dir = os.path.join('..', 'data', cfg.dataset, 'data', eval_set)

    users, groups, train_data, test_data = read_data(train_data_dir, test_data_dir)

    clients = create_clients(users, groups, train_data, test_data, model, cfg)

    return clients


def get_stat_writer_function(ids, groups, num_samples, args):

    def writer_fn(num_round, metrics, partition):
        metrics_writer.print_metrics(
            num_round, ids, metrics, groups, num_samples, partition, args.metrics_dir, '{}_{}'.format(args.metrics_name, 'stat'))

    return writer_fn


def get_sys_writer_function(args):

    def writer_fn(num_round, ids, metrics, groups, num_samples):
        metrics_writer.print_metrics(
            num_round, ids, metrics, groups, num_samples, 'train', args.metrics_dir, '{}_{}'.format(args.metrics_name, 'sys'))

    return writer_fn


def print_stats(
    num_round, server, clients, num_samples, args, writer):
    
    train_stat_metrics = server.test_model(clients, set_to_use='train')
    print_metrics(train_stat_metrics, num_samples, prefix='train_')
    writer(num_round, train_stat_metrics, 'train')

    test_stat_metrics = server.test_model(clients, set_to_use='test')
    print_metrics(test_stat_metrics, num_samples, prefix='test_')
    writer(num_round, test_stat_metrics, 'test')


def print_metrics(metrics, weights, prefix=''):
    """Prints weighted averages of the given metrics.

    Args:
        metrics: dict with client ids as keys. Each entry is a dict
            with the metrics of that client.
        weights: dict with client ids as keys. Each entry is the weight
            for that client.
    """
    client_ids = [c for c in sorted(metrics.keys())]
    ordered_weights = [weights[c] for c in client_ids]
    metric_names = metrics_writer.get_metrics_names(metrics)
    to_ret = None
    L = Logger()
    logger = L.get_logger()
    for metric in metric_names:
        ordered_metric = [metrics[c][metric] for c in client_ids]
        logger.info('%s: %g, 10th percentile: %g, 50th percentile: %g, 90th percentile %g' \
              % (prefix + metric,
                 np.average(ordered_metric, weights=ordered_weights),
                 np.percentile(ordered_metric, 10),
                 np.percentile(ordered_metric, 50),
                 np.percentile(ordered_metric, 90)))
        # print(prefix + metric)
        # for i in range(len(client_ids)):
        #     print("client_id = {}, weight = {}, {} = {}".format(client_ids[i], ordered_weights[i], prefix + metric, ordered_metric[i]))
        # print('total: {} = {}'.format(prefix + metric, np.average(ordered_metric, weights=ordered_weights)))


if __name__ == '__main__':
    # nohup python main.py -dataset shakespeare -model stacked_lstm &
    start_time=time.time()
    main()
    # logger.info("used time = {}s".format(time.time() - start_time))
