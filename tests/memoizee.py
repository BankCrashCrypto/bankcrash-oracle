#%%
from memorize import Memorize


@Memorize
def yourFunction(x, y, z):
  # do great things...
  print(x,y,z+x)
  return x,y
  

x,y,z=2, 3, 7
print(yourFunction(x,y,z))
# %%
import os

print(os.path.abspath(("memoizee.py")))
print(os.path.basename(("memoizee.py")))
# %%
from joblib import Memory
memory = Memory("cacheme.meee")

@memory.cache
def expensive_funcion(param):
  print("ok")
  return param+1
  
x=8
expensive_funcion(x)
  
# %%
