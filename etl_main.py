# %%
import pandas as pd
import numpy as np
from src import soporte as sl

# %%

df = pd.read_csv('files/finanzas-hotel-bookings.csv', index_col=0)

df = sl.drops(df)

df = sl.replaces(df)
#%%
sl.nuevas_columnas(df)
df= sl.convert_to_datetime(df)
df= sl.clean(df)
display(df)

df.to_csv("df_definitivo.csv", index=False)



# %%
