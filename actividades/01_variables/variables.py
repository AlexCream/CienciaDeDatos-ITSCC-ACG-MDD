x=5
y=-9
pi=3.1416
e=2.7182

while True:   
    a = input("Que tipo de variebles quieres ver?" \
    "\nE: Enteros"
    "\nF: Flotantes"
    "\nEXIT: Salir del programa\n")
    print("\n")

    match a.lower():
        case "e":
            print("Variables enteras:", y, x)
        case "f":
            print("Variables flotantes:", pi, e)
        case "exit":
            print("Cerrando el programa...")
            break
        case _ :
            print("Opcion no valida, intente de nuevo")
    print("\n")

