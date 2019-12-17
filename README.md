# Leaf: A Benchmark for Federated Settings

## What we have done to Leaf

Briefly speaking, we make Leaf simulate the federated learning process more in line with the fact. 

### Deadline

We add deadline setting for simulating failed upload and time out training. Now deadline follows a normal distribution in each round, and each client has the same deadline in one round. You can set the deadline's normal distribution parameters in the config file.

### Device Type

Each client is bundled with a device type. Each device type has different training speeds and uploading time. We support the small/mid/big device, whose parameter can be set in the config file. We also support self-defined device type(-1) whose parameter you can set in the code manually for more complexed simulation. Note that if a client's device is not specified i.e. None, the program will use real training time instead of the simulation time, which is not recommended.

### Round Failure

In federated settings, if there are not enough devices to upload the results in a round, then this round will be regarded as a failed round and the global model will not be updated. To simulate it, we add a update_frac parameter. If the uploaded fraction is smaller than update_frac, then this round will fail. You can also set it in the config file.

### Config

To simplify the command line arguments, we move most of the parameters to a config file. Also, we add some other parameters as put above for better simulation. Here are some details.

```bash
# -1 for unlimited, >0 for round num
num_rounds -1
# learning rate
learning_rate 0.1
# evaluate the global model's loss and accuracy every 'eval_every' round
eval_every 3
# client num per round
clients_per_round 30
# batch size
batch_size 10
# random seed
seed 0
# run 'num_epochs' epochs in one round for each client
num_epochs 1
# deadline's μ and σ
round_ddl 30 5
# least update fraction for a successful round
update_frac 0.5
# μ and σ of big device's upload time
big_upload_time 5 1
# μ and σ of mid device's upload time
mid_upload_time 10 1
# μ and σ of small device's upload time
small_upload_time 15 1
# μ and σ of big device's training speed
big_speed 150 1
# μ and σ of mid device's training speed
mid_speed 100 1
# μ and σ of small device's training speed
small_speed 50 1
```

## How to run it

```bash
git clone https://github.com/lh-ycx/leaf.git
pip3 install -r requirements.txt
cd leaf/data/shakespeare/
./preprocess.sh -s niid --sf 0.2 -k 0 -t sample -tf 0.8
cd ../../models/
python3 main.py
```

## Resources

  * **Homepage:** [leaf.cmu.edu](https://leaf.cmu.edu)
  * **Paper:** ["LEAF: A Benchmark for Federated Settings"](https://arxiv.org/abs/1812.01097)

## Datasets

1. FEMNIST

  * **Overview:** Image Dataset
  * **Details:** 62 different classes (10 digits, 26 lowercase, 26 uppercase), images are 28 by 28 pixels (with option to make them all 128 by 128 pixels), 3500 users
  * **Task:** Image Classification

2. Sentiment140

  * **Overview:** Text Dataset of Tweets
  * **Details** 660120 users
  * **Task:** Sentiment Analysis

3. Shakespeare

  * **Overview:** Text Dataset of Shakespeare Dialogues
  * **Details:** 2288 users
  * **Task:** Next-Character Prediction

4. Celeba

  * **Overview:** Image Dataset based on the [Large-scale CelebFaces Attributes Dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)
  * **Details:** 9343 users (we exclude celebrities with less than 5 images)
  * **Task:** Image Classification (Smiling vs. Not smiling)

5. Synthetic Dataset

  * **Overview:** We propose a process to generate synthetic, challenging federated datasets. The high-level goal is to create devices whose true models are device-dependant. To see a description of the whole generative process, please refer to the paper
  * **Details:** The user can customize the number of devices, the number of classes and the number of dimensions, among others
  * **Task:** Classification

6. Reddit

  * **Overview:** We preprocess the Reddit data released by [pushshift.io](https://files.pushshift.io/reddit/) corresponding to December 2017.
  * **Details:** 1,660,820 users with a total of 56,587,343 comments. 
  * **Task:** Next-word Prediction.

## Notes

- Install the libraries listed in ```requirements.txt```
    - I.e. with pip: run ```pip3 install -r requirements.txt```
- Go to directory of respective dataset for instructions on generating data
- ```models``` directory contains instructions on running baseline reference implementations
