import pandas as pd

def identificar_filas_basura(df, umbral_campos_invalidos=5):
    condiciones = pd.DataFrame()
    condiciones["age_invalida"]      = (df["age"] > 150) | (df["age"] < 0)| (df["age"].isnull())
    condiciones["sex_conditions"]          = df["sex"].isnull()
    condiciones["income_conditions"]   = (df["income"] < 0) | (df["income"].isnull())
    condiciones["height_conditions"]   = (df["height"] < 0) | (df["height"].isnull())
    condiciones["city_conditions"] = df["city"].isnull()
    condiciones["education_conditions"]   = df["education"].isnull()
    condiciones["children_conditions"] = (df["children"] < 0) | (df["children"].isnull())


    df["campos_invalidos"] = condiciones.sum(axis=1)

    filas_basura = df[df["campos_invalidos"] >= umbral_campos_invalidos]
    filas_limpias = df[df["campos_invalidos"] < umbral_campos_invalidos].drop(columns="campos_invalidos")

    return filas_limpias, filas_basura
    