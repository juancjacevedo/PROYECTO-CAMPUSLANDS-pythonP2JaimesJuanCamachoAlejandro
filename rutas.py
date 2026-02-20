# rutas.py
from UTILS.init import cargarDatos, guardarDatos

def menu_rutas():
    while True:
        print("\n" + "-"*50)
        print("GESTIÓN DE RUTAS DE ENTRENAMIENTO")
        print("-"*50)
        print("1. Registrar Ruta")
        print("2. Ver Rutas")
        print("3. Agregar Módulo a Ruta")
        print("4. Ver Módulos de una Ruta")
        print("5. Crear Área de Entrenamiento")
        print("6. Ver Áreas de Entrenamiento")
        print("7. Volver al menú principal")
        print("-"*50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_ruta()
        elif opcion == "2":
            ver_rutas()
        elif opcion == "3":
            agregar_modulo_a_ruta()
        elif opcion == "4":
            ver_modulos_ruta()
        elif opcion == "5":
            crear_area_entrenamiento()
        elif opcion == "6":
            ver_areas_entrenamiento()
        elif opcion == "7":
            break
        else:
            print("Opción inválida.")

def registrar_ruta():
    datos = cargarDatos()

    print("\n--- REGISTRAR RUTA ---")
    
    print("\nRutas disponibles:")
    print("1. NodeJS")
    print("2. Java")
    print("3. NetCore")
    
    opcion = input("\nSeleccione una ruta (1-3): ").strip()
    
    rutas_map = {
        "1": "NodeJS",
        "2": "Java",
        "3": "NetCore"
    }
    
    if opcion not in rutas_map:
        print("Opción inválida.")
        return
    
    nombre_ruta = rutas_map[opcion]

    if nombre_ruta in datos["rutas"]:
        print("La ruta ya existe.")
        return

    # Información adicional de la ruta
    print(f"\nConfigurando ruta: {nombre_ruta}")
    
    # Módulos predefinidos según la ruta
    modulos_predefinidos = {
        "NodeJS": [
            "Fundamentos de programación",
            "Introducción a la algoritmia",
            "PSeInt y Python",
            "Programación Web (HTML, CSS, Bootstrap)",
            "Bases de datos (MySQL, MongoDB, PostgreSQL)",
            "Backend (NodeJS, Express)"
        ],
        "Java": [
            "Fundamentos de programación",
            "Introducción a la algoritmia",
            "PSeInt y Python",
            "Programación formal (Java, JavaScript, C#)",
            "Bases de datos (MySQL, MongoDB, PostgreSQL)",
            "Backend (Spring Boot)"
        ],
        "NetCore": [
            "Fundamentos de programación",
            "Introducción a la algoritmia",
            "PSeInt y Python",
            "Programación formal (Java, JavaScript, C#)",
            "Bases de datos (MySQL, MongoDB, PostgreSQL)",
            "Backend (NetCore)"
        ]
    }

    datos["rutas"][nombre_ruta] = {
        "capacidad": 33,
        "campers_asignados": [],
        "trainer_asignado": None,
        "especialidad": nombre_ruta,
        "modulos": {},
        "areas_entrenamiento": []
    }
    
    # Agregar módulos predefinidos
    for i, nombre_modulo in enumerate(modulos_predefinidos[nombre_ruta], 1):
        datos["rutas"][nombre_ruta]["modulos"][f"modulo_{i}"] = {
            "nombre": nombre_modulo,
            "fecha_inicio": None,
            "fecha_fin": None,
            "completado": False
        }

    guardarDatos(datos)
    print(f"Ruta '{nombre_ruta}' registrada correctamente con {len(modulos_predefinidos[nombre_ruta])} módulos.")

def ver_rutas():
    datos = cargar_datos()

    print("\n" + "="*50)
    print("--- LISTA DE RUTAS ---")
    print("="*50)

    if not datos["rutas"]:
        print("No hay rutas registradas.")
        return

    for nombre, info in datos["rutas"].items():
        disponibles = info["capacidad"] - len(info.get("campers_asignados", []))
        print(f"\nRuta: {nombre}")
        print(f"Especialidad: {info.get('especialidad', nombre)}")
        print(f"Capacidad: {info['capacidad']}")
        print(f"Disponibles: {disponibles}")
        print(f"Campers asignados: {len(info.get('campers_asignados', []))}")
        print(f"Trainer: {info.get('trainer_asignado', 'Sin asignar')}")
        print(f"Módulos: {len(info.get('modulos', {}))}")
        print(f"Áreas de entrenamiento: {len(info.get('areas_entrenamiento', []))}")
        print("-" * 50)

def agregar_modulo_a_ruta():
    datos = cargar_datos()

    print("\n--- AGREGAR MÓDULO A RUTA ---")
    
    if not datos["rutas"]:
        print("No hay rutas registradas.")
        return

    print("\nRutas disponibles:")
    for nombre_ruta in datos["rutas"].keys():
        print(f"  • {nombre_ruta}")

    nombre_ruta = input("\nIngrese el nombre de la ruta: ").strip()

    if nombre_ruta not in datos["rutas"]:
        print("Ruta no encontrada.")
        return

    ruta = datos["rutas"][nombre_ruta]
    
    nombre_modulo = input("Nombre del módulo: ").strip()
    
    # Generar ID único para el módulo
    num_modulos = len(ruta.get("modulos", {})) + 1
    id_modulo = f"modulo_{num_modulos}"
    
    if "modulos" not in ruta:
        ruta["modulos"] = {}
    
    ruta["modulos"][id_modulo] = {
        "nombre": nombre_modulo,
        "fecha_inicio": None,
        "fecha_fin": None,
        "completado": False
    }

    guardar_datos(datos)
    print(f"Módulo '{nombre_modulo}' agregado exitosamente.")

def ver_modulos_ruta():
    datos = cargar_datos()

    print("\n--- VER MÓDULOS DE RUTA ---")
    
    if not datos["rutas"]:
        print("⚠️  No hay rutas registradas.")
        return

    print("\n📚 Rutas disponibles:")
    for nombre_ruta in datos["rutas"].keys():
        print(f"  • {nombre_ruta}")

    nombre_ruta = input("\nIngrese el nombre de la ruta: ").strip()

    if nombre_ruta not in datos["rutas"]:
        print("❌ Ruta no encontrada.")
        return

    ruta = datos["rutas"][nombre_ruta]
    modulos = ruta.get("modulos", {})

    if not modulos:
        print("Esta ruta no tiene módulos registrados.")
        return
        return

    print(f"\nMódulos de la ruta '{nombre_ruta}':")
    print("="*50)
    
    for id_modulo, info_modulo in modulos.items():
        estado = "Completado" if info_modulo.get("completado", False) else "En progreso"
        print(f"\n{info_modulo['nombre']}")
        print(f"   Estado: {estado}")
        if info_modulo.get("fecha_inicio"):
            print(f"   Inicio: {info_modulo['fecha_inicio']}")
        if info_modulo.get("fecha_fin"):
            print(f"   Fin: {info_modulo['fecha_fin']}")

def crear_area_entrenamiento():
    """
    Crea un área de entrenamiento con horarios específicos.
    Las áreas tienen capacidad de 33 campers y clases cada 4 horas.
    """
    datos = cargar_datos()

    print("\n--- CREAR ÁREA DE ENTRENAMIENTO ---")
    
    if not datos["rutas"]:
        print("No hay rutas registradas.")
        return

    print("\nRutas disponibles:")
    for nombre_ruta in datos["rutas"].keys():
        print(f"  • {nombre_ruta}")

    nombre_ruta = input("\nIngrese el nombre de la ruta: ").strip()

    if nombre_ruta not in datos["rutas"]:
        print("Ruta no encontrada.")
        return

    ruta = datos["rutas"][nombre_ruta]
    
    nombre_area = input("Nombre del área de entrenamiento: ").strip()
    
    print("\n⏰ Configurar horarios (cada área tiene clases cada 4 horas)")
    print("Horarios disponibles:")
    print("1. 6AM - 10AM")
    print("2. 10AM - 2PM")
    print("3. 2PM - 6PM")
    
    opcion_horario = input("Seleccione un horario (1-3): ").strip()
    
    horarios_map = {
        "1": {"inicio": 6, "fin": 10, "texto": "6AM - 10AM"},
        "2": {"inicio": 10, "fin": 14, "texto": "10AM - 2PM"},
        "3": {"inicio": 14, "fin": 18, "texto": "2PM - 6PM"}
    }
    
    if opcion_horario not in horarios_map:
        print("❌ Opción inválida.")
        return
    
    horario = horarios_map[opcion_horario]
    
    if "areas_entrenamiento" not in ruta:
        ruta["areas_entrenamiento"] = []
    
    # Verificar que no haya otra área en el mismo horario
    for area in ruta["areas_entrenamiento"]:
        if area["horario"]["inicio"] == horario["inicio"]:
            print(f"Ya existe un área en este horario: {area['nombre']}")
            return
    
    area = {
        "nombre": nombre_area,
        "capacidad": 33,
        "horario": horario,
        "campers": [],
        "trainer": ruta.get("trainer_asignado")
    }
    
    ruta["areas_entrenamiento"].append(area)

    guardar_datos(datos)
    print(f"Área '{nombre_area}' creada exitosamente.")
    print(f"   Horario: {horario['texto']}")
    print(f"   Capacidad: 33 campers")

def ver_areas_entrenamiento():
    datos = cargar_datos()

    print("\n--- ÁREAS DE ENTRENAMIENTO ---")
    
    if not datos["rutas"]:
        print("⚠️  No hay rutas registradas.")
        return

    hay_areas = False
    
    for nombre_ruta, info_ruta in datos["rutas"].items():
        areas = info_ruta.get("areas_entrenamiento", [])
        
        if areas:
            hay_areas = True
            print(f"\n📚 Ruta: {nombre_ruta}")
            print("="*50)
            
            for area in areas:
                print(f"\n🏫 Área: {area['nombre']}")
                print(f"   ⏰ Horario: {area['horario']['texto']}")
                print(f"   👥 Capacidad: {area['capacidad']}")
                print(f"   👨‍🎓 Campers: {len(area.get('campers', []))}/{area['capacidad']}")
                print(f"   👨‍🏫 Trainer: {area.get('trainer', 'Sin asignar')}")
    
    if not hay_areas:
        print("⚠️  No hay áreas de entrenamiento creadas.")
