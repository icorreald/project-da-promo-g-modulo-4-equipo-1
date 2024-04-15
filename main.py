# %%
# Importaciones 
from src import limpieza as sp
import pandas as pd
import numpy as np

#Abrimos CSV:
df = pd.read_csv('files/finanzas-hotel-bookings.csv', index_col=0)

#Funcion para explorar el dataframe
sp.exploracion(df)
df

#Ponemos en minúsculas el contenido de DF
sp.minusculas(df)
df

sp.limpiar_valores(df)
df.shape

#guardar dataframe final 
df.to_csv("df_final_prueba.csv")

df.head()
