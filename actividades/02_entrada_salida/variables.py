def ImprimeDatos(nombre, apellido, edad, estatura):
    print("\n")
    print("Nombre:", nombre)
    print("Apellido:", apellido)
    MayorDeEdad(edad)
    print("Estatura:"+str(estatura)+" metros")
    print("\n")

def MayorDeEdad(edad):
    if edad >= 18:
        print("Edad:", edad, "eres mayor de edad")
    else:
        print("Edad:", edad, "eres menor de edad")

def getNombre(palabra):
    nombre = input("Ingrese su " + palabra + ": ")

    if nombre.isalpha():
        if nombre == "":
            print("Error: El " + palabra + " no puede estar vacío. Intente de nuevo.")
            return getNombre(palabra)
        else:
            return nombre
    else:
        print("Error: El " + palabra + " debe contener solo letras. Intente de nuevo.")
        return getNombre(palabra)
    
def getEdad():
    edadaux = input("Ingrese su edad en años: ")

    if edadaux.isdigit():
        edad = int(edadaux)
    else:
        print("Error: La edad debe ser un número válido. Intente de nuevo.")
        return getEdad()
    
    if edad < 0:
        print("Error: La edad no puede ser negativa. Intente de nuevo.")
        return getEdad()
    else:
        return edad
    
def getEstatura():
    estaturaAux = input("Ingrese su estatura en metros: ")

    if estaturaAux.replace('.', '', 1).isdigit():
        estatura = float(estaturaAux)
    else:
        print("Error: La estatura debe ser un número válido. Intente de nuevo.")
        return getEstatura()
    
    if estatura <= 0:
        print("Error: La estatura no puede ser negativa o cero. Intente de nuevo.")
        return getEstatura()
    else:
        return estatura
    
ImprimeDatos(getNombre("nombre"), getNombre("apellido"), getEdad(), getEstatura())