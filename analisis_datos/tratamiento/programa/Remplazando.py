import numpy as np
import pandas as pd
from scipy import stats

def TratamientoIncome(df):
   dftratado = df.copy()
   dftratado.loc[(dftratado["age"] < 20) & (dftratado["age"] > -1) & (dftratado["income"] < 0), "income"] = 0
   return dftratado

def TratarEdad(df, discriminacion=2):
    df_tratado = df.copy()
    
    # Corregir negativos a 0
    df_tratado.loc[df_tratado["age"] < 0, "age"] = 0
    
    # Obtener valores no nulos y calcular z-score
    age_validos = df_tratado["age"].dropna()
    z_scores = pd.Series(np.abs(stats.zscore(age_validos)), index=age_validos.index)
    
    # Limite superior válido
    limite_superior = df_tratado.loc[z_scores < discriminacion, "age"].max()
    if pd.isna(limite_superior):
        limite_superior = age_validos.median()  
        
    df_tratado.loc[z_scores >= discriminacion, "age"] = limite_superior

    return df_tratado

def TratamientoSexo(data_treated_age):
    data_treated_sex = data_treated_age.copy()
    mapa_sex = {
        "male": "Male", "m": "Male", "man": "Male", "mal": "Male",
        "female": "Female", "f": "Female", "woman": "Female",
        "femal": "Female", "famale": "Female",
    }
    data_treated_sex["sex"] = (
        data_treated_sex["sex"]
        .str.strip().str.lower()
        .map(lambda x: mapa_sex.get(x, x) if pd.notna(x) else "No especificado")
    )
    return data_treated_sex

def TratamientoChildren(data_treated_sex):
    data_treated_children = data_treated_sex.copy()
    data_treated_children.loc[data_treated_children["children"].isnull() | data_treated_children["children"] < 0, "children"] = 0
    return data_treated_children

def TratamientoEducation(data_treated_children):
    data_treated_education = data_treated_children.copy()
    mapa_edu = {
        "phd": "PhD", "ph.d": "PhD", "ph.d.": "PhD", "ph d": "PhD",
        "master": "Master", "masters": "Master", "mastre": "Master",
        "maste": "Master", "máster": "Master",
        "bachelor": "Bachelor", "bachelors": "Bachelor",
        "bachelo": "Bachelor", "bacheler": "Bachelor",
        "none": "None", "no": "None", "n/a": "None",
        "sin educacion": "None",
    }
    data_treated_education["education"] = (
        data_treated_education["education"]
        .str.strip().str.lower()
        .map(lambda x: mapa_edu.get(x, x) if pd.notna(x) else "No especificado")
    )
    return data_treated_education