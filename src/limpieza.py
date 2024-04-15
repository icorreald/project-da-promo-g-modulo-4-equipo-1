#IMPORTACIONES

import pandas as pd
import numpy as np
import random
from datetime import date

#------------------------------------------------------------------------
import scipy.stats as stats
from scipy.stats import shapiro
from scipy.stats import mannwhitneyu
import re
import os #Operating system para encontrar el archivo en distintos sistemas operativos 

# -----------------------------------------------------------------------
pd.set_option('display.max_columns', None) 
import warnings
warnings.filterwarnings("ignore")

#función para leer los CSV
def leer_cvs(carpeta, nombre_archivo, drop_unnamed=True):
    '''
    Abre y lee los documentos CSV. 
        Si el archivo se encuentra, lo abre en un DataFrame de pandas y lo devuelve. 
        Si el archivo no se encuentra, la función imprime un mensaje indicando que el archivo no se encontró y devuelve None.
    
    Esta función toma el nombre de una carpeta y el nombre de archivo como entrada y lee el archivo CSV.
    
    Args:
        carpeta (str): El nombre de la carpeta donde se encuentra el archivo.
        nombre_archivo (str): El nombre del archivo csv sin la extensión.
        drop_unnamed (bool, opcional): Indica si se debe excluir la columna 'Unnamed' al leer el archivo CSV. Por defecto es True.

    Returns:
        pd.DataFrame: Un DataFrame que contiene los datos del archivo csv, o None si el archivo no se encuentra.
    '''
    df = pd.read_csv(os.path.join(carpeta, nombre_archivo))
    print('El archivo se ha cargado con éxito.')

    if drop_unnamed:
        df = df.drop(columns=["Unnamed: 0"], errors="ignore")  # Ignora si la columna no existe
        
    return df
    
def exploracion (df):
        
        print(f"INFORMACIÓN SOBRE HOTEL")
        print(f"La forma:")
        print(f"{df.shape}\n")
        print(f"Las columnas:")
        print(f"{df.columns}\n")
        print(f"Los tipos de datos:")
        print(f"{df.dtypes}\n")
        print(f"Los nulos:")
        print(f"{df.isnull().sum()}\n")
        print(f"Los duplicados:")
        print(f"{df.duplicated().sum()}\n")
        print(f"Los principales estadísticos:")
        print(f"{df.describe().T}\n")
        print(f"\n-----------------------------\n")
    
        return df
    
    

def minusculas(dataframe):
    '''
    Convierte todos los valores del DataFrame a minúsculas.

    Args:
        dataframe (pd.DataFrame): El DataFrame que se desea modificar.

    Returns:
        None: La función modifica el DataFrame original inplace.
    '''
    
    # Iterar sobre cada columna
    for col in dataframe.columns:
        # Verificar si la columna contiene strings y convertirlos a minúsculas
        if dataframe[col].dtype == 'object':
            dataframe[col] = dataframe[col].astype(str).str.lower()


def limpiar_valores(df):
    '''
    Limpia los valores de todas las columnas de un DataFrame reemplazando caracteres específicos.

    Args:
        df (pd.DataFrame): El DataFrame que se desea limpiar.

    Returns:
        None: La función modifica el DataFrame original inplace.
    '''
    # eliminar duplicados
    df.drop_duplicates(inplace=True)

    #Quitamos Nan columna "hotel"
    df['hotel'].fillna('UNK', inplace=True)
    indices = df[df['hotel']=='UNK'].index
    df.drop(indices, axis=0, inplace=True)

    # Iterar sobre cada columna del DataFrame
    integers= ["required_car_parking_spaces", "days_in_waiting_list", "total_of_special_requests"]
    for columna in integers:
        #convierte los valores de la columna a enteros
        #mantiene los valores NaN con NaN 
        df[columna] = df[columna].astype('Int64', errors= 'ignore')


    # Mapear los números de mes a nombres de mes
    meses = {
        '1': 'January',
        '2': 'February',
        '3': 'March',
    }
    df['arrival_date_month'] = df['arrival_date_month'].astype(str)
    df['arrival_date_month'] = df['arrival_date_month'].replace(meses)

    # Cambiamos los valores de 'repeted'
    repeted = {1 :'True', 0 : 'False', np.nan : np.nan}
    df["is_repeated_guest"]=df["is_repeated_guest"].map(repeted)
    

    # eliminar la columna company por el alto % de nulos (96.74%),a sícomo otras columnas que tienen 40% nulos o mas 
    df.drop(columns=['company',"market_segment", 'reserved_room_type', '0'], inplace=True)

    df.rename(columns={'adr': 'average_daily_rate'}, inplace=True)

    # Convertir 'reservation_status_date' a tipo datetime, manejar fechas inválidas
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce').dt.date

    # Reemplazar fechas inválidas con NaN
    df['reservation_status_date'] = df['reservation_status_date'].replace(pd.NaT, np.nan)

    