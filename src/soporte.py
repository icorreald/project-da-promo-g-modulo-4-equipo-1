import pandas as pd
import numpy as np
from datetime import date

def lead_time(valor):
    if valor > 365:
        return '> 12 meses'
    elif valor > 330:
        return '> 11 meses'
    elif valor > 300:
        return '> 10 meses'
    elif valor > 270:
        return '> 9 meses'
    elif valor > 240:
        return '> 8 meses'
    elif valor > 210:
        return '> 7 meses'
    elif valor > 180:
        return '> 6 meses'
    elif valor > 150:
        return '> 5 meses'
    elif valor > 120:
        return '> 4 meses'
    elif valor > 90:
        return '> 3 meses'
    elif valor > 60:
        return '> 2 meses'
    elif valor > 30:
        return '> 1 mes'
    else:
        return '< 1 mes'

    
def drops(df):
    df.drop_duplicates(inplace=True)

    df.drop(columns=['company', "market_segment", '0','reserved_room_type'], inplace=True)

    indices = df[df['hotel'].isna()].index
    df.drop(indices, axis=0, inplace=True)

    df.reset_index()

    return df


def replaces(df):
    # Mapear los números de mes a nombres de mes
    meses = {
        '1': 'January',
        '2': 'February',
        '3': 'March',}

    df['arrival_date_month'] = df['arrival_date_month'].astype(str)
    df['arrival_date_month'] = df['arrival_date_month'].replace(meses)

    # Cambiamos los valores de 'repeted'
    values = {1 :'True', 0 : 'False', np.nan : np.nan}
    df["is_repeated_guest"] = df["is_repeated_guest"].map(values)
    df['is_repeated_guest'].unique()

    # cambiamos nombre a adr
    df.rename(columns={'adr': 'average daily rate'}, inplace=True)

    df['lead_time_months'] = df['lead_time'].apply(lead_time)
    df['ltm'] = df['lead_time_months']
    df['ltm']=df['ltm'].map({'< 1 mes': 0,
               '> 1 mes': 1,
               '> 2 meses': 2,
               '> 3 meses': 3,
               '> 4 meses': 4,
               '> 5 meses': 5,
               '> 6 meses': 6,
               '> 7 meses': 7,
               '> 8 meses': 8,
               '> 9 meses': 9,
               '> 10 meses': 10,
               '> 11 meses': 11,
               '> 12 meses': 12
              })
   
    return df


def to_int(valor):
    try:
        return int(valor.replace(',','.'))
    except:
        return valor

def col_to_int(df, lista_col):
    for col in lista_col:
        df[col] = df[col].apply(to_int)

# renombrar columnas
def nuevas_columnas(df):
    nuevas_columnas = {columna: columna.lower() for columna in df.columns}
    return df.rename(columns=nuevas_columnas, inplace= True)

# string to lower
def unify(valor):
    try:
        return valor.lower().strip()
    except:
        return valor

# aplicar cambios a df    
def homog_tablas(lista_df):
    for df in lista_df:
        nuevas_columnas(df)
    
    for df in lista_df:
        for columna in df.columns:
            df[columna] = df[columna].apply(unify)


def convert_to_datetime(df):
    
    # Convertir la columna especificada a tipo datetime y manejar fechas inválidas
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce').dt.date
    
    return df


def clean(df):
    """
    Elimina las filas donde 'average daily rate' es menor o igual a cero.
    
    Parámetros:
    df (DataFrame): DataFrame de entrada
    
    Devuelve:
    DataFrame: DataFrame limpio sin las filas donde 'average daily rate' es menor o igual a cero.
    """
    # Seleccionar las filas donde 'average daily rate' es menor o igual a cero y obtener sus índices
    rows_to_drop = df[df["average daily rate"] <= 0].index

    # Eliminar las filas con los índices seleccionados
    df_cleaned = df.drop(rows_to_drop)

    return df_cleaned

