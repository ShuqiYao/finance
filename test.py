#%% test
import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt



#%%
basics_data = ts.get_stock_basics()

#%%
basics_data.head()

#%%
np.average(basics_data['pe'])

#%%
basics_data['pe'].describe()

#%%
plt.plot(basics_data['pe'])

#%%
