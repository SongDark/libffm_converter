import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import subprocess,time
from matplotlib import pyplot as plt
from scipy.optimize import leastsq

data = pd.read_csv("test.csv")

records=[]
for i in range(1000, 5200, 200):
    
    df = pd.DataFrame(np.tile(data, (i,1)), columns=data.columns)
    df.to_csv("time_test/test.csv", index=False)
    
    start1 = time.time()
    cmd = 'python {par} {cvt} {src} {des} -n {nr_thread}'.format(par='libffm_parallelizer.py', cvt='libffm_converter.py', src='time_test/test.csv', des='time_test/test.ffm', nr_thread=16)
    subprocess.call(cmd, shell=True)
    end1 = time.time()
    
    start2 = time.time()
    cmd = 'python {cvt} {src} {des}'.format(cvt='libffm_converter.py', src='time_test/test.csv', des='time_test/test.ffm', nr_thread=16)
    subprocess.call(cmd, shell=True)
    end2 = time.time()

    records.append([df.shape[0], end1-start1, end2-start2])

    print i, df.shape

records = np.array(records)
plt.plot(records[:,0], records[:,1], label='parallel')
plt.plot(records[:,0], records[:,2], label='serial')
plt.legend()
plt.xlabel("data shape")
plt.ylabel('seconds')
plt.savefig('./time_test/res.png')

np.save('./time_test/records.npy',records)
 
def residuals_func(p, y, x):  
    ret = fit_func(p, x) - y  
    return ret

def fit_func(p, x):  
    f = np.poly1d(p)  
    return f(x)

records = np.load('./time_test/records.npy')
n = 2
plsq = leastsq(residuals_func, np.random.randn(n), args=(records[:,1], records[:,0]))
plt.plot(records[:,0], fit_func(plsq[0], records[:,0]), label='fit_parallel') 
plt.plot(records[:,0], records[:,1], label='real_parallel')
print plsq[0], fit_func(plsq[0], [1e8])
plsq = leastsq(residuals_func, np.random.randn(n), args=(records[:,2], records[:,0]))
plt.plot(records[:,0], fit_func(plsq[0], records[:,0]), label='fit_serial') 
plt.plot(records[:,0], records[:,2], label='real_serial') 
print plsq[0] , fit_func(plsq[0], [1e8])
plt.legend()
plt.savefig('./time_test/ploy.png')
