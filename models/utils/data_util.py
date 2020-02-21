import json
import numpy as np
import os

input_dir = '../../data/reddit/data/train/'

def read_dir(data_dir):
    num_sample = []

    files = os.listdir(data_dir)
    files = [f for f in files if f.endswith('.json')]
    for f in files:
        file_path = os.path.join(data_dir,f)
        with open(file_path, 'r') as inf:
            cdata = json.load(inf)
        num_sample.extend(cdata['num_samples'])

    return num_sample

if __name__ == "__main__":
    num_sample = read_dir(input_dir)
    print(np.percentile(num_sample, 90))

