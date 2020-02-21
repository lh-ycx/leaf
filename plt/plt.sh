#! /bin/sh
datasets="reddit celeba"
for dataset in $datasets
do
python loss_by_time.py $dataset
python loss_by_round.py $dataset
python acc@1_by_round.py $dataset
python acc@1_by_time.py $dataset
done

python comp_distribution.py
python acc_distribution.py