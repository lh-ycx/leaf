import os

dates = [str(date) for date in range(20200123,20200130)]

print('dates:{}'.format(dates))
for date in dates:
    cur_dir = 'cdate={}'.format(date)
    print('process {}...'.format(cur_dir))
    os.system('aws s3 cp s3://nlptech-cube/tmp_fed_train_data/appkey=27ce35fb228faeb5f2ed8beec9d44ebe/{} {} --recursive'.format(cur_dir,cur_dir))
    retval = os.getcwd()
    os.chdir(cur_dir)
    os.system('gzip -d -f *')
    os.chdir(retval)
    