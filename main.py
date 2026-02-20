# main.py
from UTILS.init import cargarDatos, guardarDatos
from campers import menu_campers
from trainers import menu_trainers
from rutas import menu_rutas
from coordinador import menu_coordinador
from reportes import menu_reportes

def menu_principal():
    while True:
        print("\n" + "="*50)
        print("===== SISTEMA DE GESTIÓN CAMPUSLANDS =====")
        print("="*50)
        print("\nSELECCIONE SU ROL:")
        print("-"*50)
        print("1. ROL CAMPER - Gestión de Campers")
        print("2. ROL TRAINER - Gestión de Trainers")
        print("3. ROL COORDINADOR - Coordinacion Academica")
        print("4. Menu Rutas de Entrenamiento")
        print("5. Reportes del Sistema")
        print("6. Salir")
        print("="*50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_campers()
        elif opcion == "2":
            menu_trainers()
        elif opcion == "3":
            menu_rutas()
        elif opcion == "4":
            menu_coordinador()
        elif opcion == "5":
            menu_reportes()
        elif opcion == "6":
            print("\n¡Gracias por usar el sistema CampusLands!")
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    datos = cargarDatos()
    menu_principal()
