import numpy as np
import pandas as pd

s = '1,2,3,4,5,6,7,8,9,10'
print ('string: '+str(s.__sizeof__())+'\n')
l = [1,2,3,4,5,6,7,8,9,10]
print ('list: '+str(l.__sizeof__())+'\n')
a = np.array([1,2,3,4,5,6,7,8,9,10])
print ('array: '+str(a.__sizeof__())+'\n')
b = np.array([1,2,3,4,5,6,7,8,9,10], dtype=np.dtype('u1'))
print ('byte array: '+str(b.__sizeof__())+'\n')
df = pd.DataFrame([1,2,3,4,5,6,7,8,9,10])
print ('dataframe: '+str(df.__sizeof__())+'\n')