import os
import subprocess
import math
import hashlib

def hashstr(S, nr_bins):
    return str(int(hashlib.md5(S.encode('utf-8')).hexdigest(), 16)%(nr_bins-1) + 1)

def delete(path, nr_thread):
    for i in range(nr_thread):
        os.remove('{0}.__tmp__.{1}'.format(path, i))

def cat(path, nr_thread):
    if os.path.exists(path):
        os.remove(path)
    
    for i in range(nr_thread):
        cmd = 'sudo cat {0}.__tmp__.{1} >> {0}'.format(path, i)
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()

def parallel_convert(converter, arg_paths, nr_thread):
    workers = []
    for i in range(nr_thread):
        cmd = "python " + converter
        for path in arg_paths:
            cmd += ' {0}'.format(path+".__tmp__.{0}".format(i)) 
        
        worker = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        workers.append(worker)
    for worker in workers:
        worker.communicate()

def open_with_first_line_skipped(path, skip=True):
        f = open(path)
        if not skip:
            return f
        next(f)
        return f

def split_csv(path, nr_thread, has_header):

    def calc_nr_lines_per_thread():
        nr_lines = int(list(subprocess.Popen('sudo wc -l {0}'.format(path), shell=True, stdout=subprocess.PIPE).stdout)[0].split()[0])
        if not has_header:
            nr_lines += 1
        return nr_lines/nr_thread
    
    def open_with_header_written(path, idx, header):
        f = open(path+'.__tmp__.{0}'.format(idx), 'w')
        if not has_header:
            return f
        f.write(header)
        return f

    header = open(path).readline()

    nr_lines_per_thread = calc_nr_lines_per_thread()

    idx = 0
    f = open_with_header_written(path, idx, header)
    for i, line in enumerate(open_with_first_line_skipped(path, has_header), start=1):
        f.write(line)
        if i % nr_lines_per_thread == 0:
            if idx < nr_thread - 1:
                f.close()
                idx += 1
                f = open_with_header_written(path, idx, header)
    f.close()