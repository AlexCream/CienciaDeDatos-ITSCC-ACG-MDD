import numpy as np
import pandas as pd
from EliminarBasura import identificar_filas_basura
from Remplazando import TratamientoSexo, TratamientoIncome, TratarEdad, TratamientoChildren, TratamientoEducation

def FuncionDeLimpiezaEspecifica(data_raw, basura = 3, exactitud = 2):

    data_no_trash, data_trash = identificar_filas_basura(data_raw, basura)

    # PRETRATAMIENTO
    data_treated_age = TratarEdad(data_no_trash, exactitud)
    data_treated_income = TratamientoIncome(data_treated_age)
    data_treated_sex = TratamientoSexo(data_treated_income)
    data_treated_children = TratamientoChildren(data_treated_sex)
    data_treated_education = TratamientoEducation(data_treated_children)
    data_clean = data_treated_education.copy()
    return data_clean

