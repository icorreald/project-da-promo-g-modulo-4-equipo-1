import pandas as pd
import numpy as np

def drops(df):
    df.drop_duplicates(inplace=True)

    df.drop(columns=['company', "market_segment", '0'], inplace=True)

    indices = df[df['hotel'].isna()].index
    df.drop(indices, axis=0, inplace=True)

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

lista_int = ["required_car_parking_spaces", "days_in_waiting_list", "total_of_special_requests"]