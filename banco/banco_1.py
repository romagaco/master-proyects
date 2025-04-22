1def mostar_saldo(saldo):
    print(f"Tu saldo actual es: {saldo:.2f}$")

def depositar():
    monto = float(input("Introduce una cantidad para depositar: "))
    if monto < 0:
        print("La cantidad introducida no es valida.")
        return 0
    else:
        return monto

def retirar(saldo):
    monto = float(input("Introduce una cantidad para retirar: "))
    if monto > saldo:
        print("Fondos insuficientes.")
        return 0
    elif monto < 0:
        print("La cantidad debe de ser mayor a 0.")
        return 0
    else:
        return monto

def menu_principal():
    saldo = 0
    en_ejecuion = True

    while en_ejecuion:
        print("Programa Bancario")
        print("1. Mostrar saldo")
        print("2. Depositar")
        print("3. Retirar")
        print("4. Salir")

        opcion = input("Introduce tu eleccion (1-4): ")
        if opcion == "1":
            mostar_saldo(saldo)
        elif opcion == "2":
            saldo += depositar()
        elif opcion == "3":
            saldo -= retirar(saldo)
        elif opcion == "4":
            en_ejecuion = False
            print("Que tengas un buen dia")
        else:
            print("Opcion no valida, escoje entre 1-4: ")

if __name__ == "__main__":
    menu_principal()




