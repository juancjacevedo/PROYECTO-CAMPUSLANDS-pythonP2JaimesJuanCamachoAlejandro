# campers.py
from campers import cargar_datos, guardar_datos

def menuCampers():
    while True:
        print("\n" + "-"*50)
        print("ROL: CAMPER - GESTIÓN DE CAMPERS")
        print("-"*50)
        print("1. Registrar Camper")
        print("2. Ver Campers")
        print("3. Actualizar Camper")
        print("4. Eliminar Camper")
        print("5. Cambiar Estado de Camper")
        print("6. Asignar Camper a Ruta")
        print("7. Volver al menú principal")
        print("-"*50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_camper()
        elif opcion == "2":
            ver_campers()
        elif opcion == "3":
            actualizar_camper()
        elif opcion == "4":
            eliminar_camper()
        elif opcion == "5":
            cambiar_estado_camper()
        elif opcion == "6":
            asignar_camper_a_ruta()
        elif opcion == "7":        
            break
        else:
            print("Opción inválida.")

def registrar_camper():
    datos = cargar_datos()

    print("\n--- REGISTRO DE CAMPER ---")

    id_camper = input("Documento del camper: ").strip()

    if id_camper in datos["campers"]:
        print("Ese documento ya existe.")
        return

    nombre = input("Nombre completo: ").strip()
    apellidos = input("Apellidos: ").strip()
    direccion = input("Dirección: ").strip()
    acudiente = input("Acudiente: ").strip()
    telefono_celular = input("Teléfono celular: ").strip()
    telefono_fijo = input("Teléfono fijo (opcional): ").strip()

    datos["campers"][id_camper] = {
        "nombre": nombre,
        "apellidos": apellidos,
        "direccion": direccion,
        "acudiente": acudiente,
        "telefono_celular": telefono_celular,
        "telefono_fijo": telefono_fijo,
        "estado": "Inscrito",
        "riesgo": "Bajo",
        "ruta_asignada": None,
        "trainer_asignado": None,
        "modulos": {},
        "nota_final": 0
    }

    guardar_datos(datos)
    print("Camper registrado exitosamente.")

def ver_campers():
    datos = cargar_datos()

    print("\n" + "="*50)
    print("--- LISTA DE CAMPERS ---")
    print("="*50)

    if not datos["campers"]:
        print("No hay campers registrados.")
        return

    for id_camper, info in datos["campers"].items():
        print(f"\nID: {id_camper}")
        print(f"Nombre: {info['nombre']} {info.get('apellidos', '')}")
        print(f"Dirección: {info['direccion']}")
        print(f"Acudiente: {info['acudiente']}")
        print(f"Teléfono: {info.get('telefono_celular', 'N/A')}")
        print(f"Estado: {info['estado']}")
        print(f"Riesgo: {info['riesgo']}")
        print(f"Ruta: {info.get('ruta_asignada', 'Sin asignar')}")
        print(f"Trainer: {info.get('trainer_asignado', 'Sin asignar')}")
        if info.get('nota_final', 0) > 0:
            print(f"Nota Final: {info['nota_final']:.2f}")
        print("-" * 50)

def actualizar_camper():
    datos = cargar_datos()

    print("\n--- ACTUALIZAR CAMPER ---")
    id_camper = input("Ingrese el ID del camper a actualizar: ").strip()

    if id_camper not in datos["campers"]:
        print("Camper no encontrado.")
        return

    camper = datos["campers"][id_camper]

    print("\nDeje en blanco si no desea cambiar el dato.")

    nombre = input(f"Nombre ({camper['nombre']}): ").strip()
    apellidos = input(f"Apellidos ({camper.get('apellidos', '')}): ").strip()
    direccion = input(f"Dirección ({camper['direccion']}): ").strip()
    acudiente = input(f"Acudiente ({camper['acudiente']}): ").strip()
    telefono_celular = input(f"Teléfono celular ({camper.get('telefono_celular', '')}): ").strip()

    if nombre:
        camper["nombre"] = nombre
    if apellidos:
        camper["apellidos"] = apellidos
    if direccion:
        camper["direccion"] = direccion
    if acudiente:
        camper["acudiente"] = acudiente
    if telefono_celular:
        camper["telefono_celular"] = telefono_celular

    guardar_datos(datos)
    print("Camper actualizado correctamente.")

def eliminar_camper():
    datos = cargar_datos()

    print("\n--- ELIMINAR CAMPER ---")
    id_camper = input("Ingrese el ID del camper a eliminar: ").strip()

    if id_camper not in datos["campers"]:
        print("Camper no encontrado.")
        return

    confirmacion = input("¿Está seguro que desea eliminar este camper? (s/n): ").strip().lower()

    if confirmacion == "s":
        del datos["campers"][id_camper]
        guardar_datos(datos)
        print("Camper eliminado correctamente.")
    else:
        print("Operación cancelada.")

def cambiar_estado_camper():
    """Permite cambiar el estado de un camper (Inscrito -> Aprobado -> Cursando, etc.)"""
    datos = cargar_datos()

    print("\n--- CAMBIAR ESTADO DE CAMPER ---")
    id_camper = input("Ingrese el ID del camper: ").strip()

    if id_camper not in datos["campers"]:
        print("Camper no encontrado.")
        return

    camper = datos["campers"][id_camper]
    
    print(f"\nEstado actual: {camper['estado']}")
    print("\nEstados disponibles:")
    print("1. Inscrito")
    print("2. Aprobado")
    print("3. Cursando")
    print("4. Graduado")
    print("5. Expulsado")
    print("6. Retirado")

    opcion = input("\nSeleccione el nuevo estado: ").strip()

    estados = {
        "1": "Inscrito",
        "2": "Aprobado",
        "3": "Cursando",
        "4": "Graduado",
        "5": "Expulsado",
        "6": "Retirado"
    }

    if opcion in estados:
        camper["estado"] = estados[opcion]
        guardar_datos(datos)
        print(f"Estado actualizado a: {estados[opcion]}")
    else:
        print("Opción inválida.")

def asignar_camper_a_ruta():
    """Asigna un camper aprobado a una ruta de entrenamiento"""
    datos = cargar_datos()

    print("\n--- ASIGNAR CAMPER A RUTA ---")
    
    # Mostrar campers aprobados
    print("\nCampers disponibles (Estado: Aprobado):")
    campers_aprobados = {id_c: info for id_c, info in datos["campers"].items() 
                         if info["estado"] == "Aprobado"}
    
    if not campers_aprobados:
        print("No hay campers en estado 'Aprobado'.")
        return

    for id_c, info in campers_aprobados.items():
        print(f"  • {id_c} - {info['nombre']} {info.get('apellidos', '')}")

    id_camper = input("\nIngrese el ID del camper: ").strip()

    if id_camper not in campers_aprobados:
        print("Camper no encontrado o no está en estado 'Aprobado'.")
        return

    # Mostrar rutas disponibles
    print("\nRutas disponibles:")
    if not datos["rutas"]:
        print("No hay rutas registradas. Regístrelas primero.")
        return

    for nombre_ruta, info_ruta in datos["rutas"].items():
        disponibles = info_ruta["capacidad"] - len(info_ruta.get("campers_asignados", []))
        print(f"  • {nombre_ruta} - Disponibles: {disponibles}/{info_ruta['capacidad']}")

    nombre_ruta = input("\nIngrese el nombre de la ruta: ").strip()

    if nombre_ruta not in datos["rutas"]:
        print("Ruta no encontrada.")
        return

    ruta = datos["rutas"][nombre_ruta]
    
    # Verificar capacidad
    if "campers_asignados" not in ruta:
        ruta["campers_asignados"] = []
    
    if len(ruta["campers_asignados"]) >= ruta["capacidad"]:
        print("La ruta ha alcanzado su capacidad máxima.")
        return

    # Asignar
    ruta["campers_asignados"].append(id_camper)
    datos["campers"][id_camper]["ruta_asignada"] = nombre_ruta
    datos["campers"][id_camper]["estado"] = "Cursando"
    
    # Asignar trainer si la ruta tiene uno
    if ruta.get("trainer_asignado"):
        datos["campers"][id_camper]["trainer_asignado"] = ruta["trainer_asignado"]

    guardar_datos(datos)
    print(f"Camper asignado exitosamente a la ruta '{nombre_ruta}'.")
