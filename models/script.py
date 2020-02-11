import os

ddls = [40,50,60,70,80,90,100,110,120,150,180,300,600,1800]
Es = [5,20]
input_dir = 'no_training.cfg'
if __name__ == "__main__":
    for E in Es:
        with open(input_dir, 'r') as f:
            all_lines = []
            for line in f:
                line = line.split()
                if line[0] == 'num_epochs':
                    line[1] = str(E)
                if line[0] == 'round_ddl':
                    line[1] = str(24*E)
                line.append('\n')
                line = ' '.join(line)
                all_lines.append(line)
        
        with open(input_dir, 'w') as f:
            for line in all_lines:
                f.write(line)

        os.system('python main.py')
        os.system('mv no_training.log reddit_trace_{}.log'.format(E))
        os.system('mv client2cnt.json client2cnt_reddit_trace_{}.json'.format(E))
        
