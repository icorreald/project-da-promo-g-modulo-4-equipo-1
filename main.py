# Importaciones 
from src import limpieza as sp

#Abrimos CSV:
df = sp.leer_cvs("files", "finanzas-hotel-bookings.csv")

#Funcion para explorar el dataframe
sp.exploracion(df)
df

#Ponemos en minúsculas el contenido de DF
sp.minusculas(df)
df

sp.limpiar_valores(df)
df.shape

#guardar dataframe final 
df.to_csv("df_final.csv")

df.head()
