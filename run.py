import subprocess, time

# Parallel
start = time.time()

cmd = 'python {par} {cvt} {src} {des} -n {nr_thread}'.format(par='libffm_parallelizer.py', cvt='libffm_converter.py', src='test.csv', des='test.ffm', nr_thread=16)

subprocess.call(cmd, shell=True)

print time.time() - start, 'sec'

# # Serial
# start = time.time()

# cmd = 'python {cvt} {src} {des}'.format(cvt='libffm_converter.py', src='test.csv', des='test1.ffm', nr_thread=16)

# subprocess.call(cmd, shell=True)

# print time.time() - start, 'sec'