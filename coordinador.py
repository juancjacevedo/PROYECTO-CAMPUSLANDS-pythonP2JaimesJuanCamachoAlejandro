# coordinador.py
from UTILS.init import cargarDatos, guardarDatos

def menu_coordinador():
    """
    Menú de coordinación académica.
    El coordinador puede registrar notas y gestionar el estado de los campers.
    """
    while True:
        print("\n" + "-"*50)
        print("ROL: COORDINADOR - COORDINACIÓN ACADÉMICA")
        print("-"*50)
        print("(Funciones exclusivas del Coordinador)")
        print("-"*50)
        print("1. Registrar/Actualizar Notas de Camper")
        print("2. Ver Notas de Camper")
        print("3. Aprobar Campers (Inscrito → Aprobado)")
        print("4. Ver Campers en Riesgo")
        print("5. Crear Matrícula de Módulo")
        print("6. Evaluar Rendimiento de Ruta")
        print("7. Volver al menú principal")
        print("-"*50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_notas()
        elif opcion == "2":
            ver_notas_camper()
        elif opcion == "3":
            aprobar_campers()
        elif opcion == "4":
            ver_campers_en_riesgo()
        elif opcion == "5":
            crear_matricula_modulo()
        elif opcion == "6":
            evaluar_rendimiento_ruta()
        elif opcion == "7":
            break
        else:
            print("Opción inválida.")

def registrar_notas():
    """
    Registra las notas de un camper en un módulo específico.
    Sistema de evaluación: 30% teórica, 60% práctica, 10% quices
    """
    datos = cargarDatos()

    print("\n--- REGISTRAR/ACTUALIZAR NOTAS ---")
    
    # Mostrar campers que están cursando
    campers_cursando = {id_c: info for id_c, info in datos["campers"].items() 
                        if info.get("estado") in ["Cursando", "Aprobado"]}
    
    if not campers_cursando:
        print("No hay campers en estado 'Cursando' o 'Aprobado'.")
        return

    print("\nCampers disponibles:")
    for id_c, info in campers_cursando.items():
        ruta = info.get("ruta_asignada", "Sin ruta")
        print(f"  • {id_c} - {info['nombre']} {info.get('apellidos', '')} - Ruta: {ruta}")

    id_camper = input("\nIngrese el ID del camper: ").strip()

    if id_camper not in campers_cursando:
        print("Camper no encontrado o no está cursando.")
        return

    camper = datos["campers"][id_camper]
    ruta_asignada = camper.get("ruta_asignada")
    
    if not ruta_asignada or ruta_asignada not in datos["rutas"]:
        print("El camper no tiene una ruta asignada válida.")
        return

    # Mostrar módulos de la ruta
    ruta = datos["rutas"][ruta_asignada]
    modulos = ruta.get("modulos", {})
    
    if not modulos:
        print("Esta ruta no tiene módulos registrados.")
        return

    print(f"\nMódulos de la ruta '{ruta_asignada}':")
    for id_mod, info_mod in modulos.items():
        print(f"  • {id_mod}: {info_mod['nombre']}")

    id_modulo = input("\nIngrese el ID del módulo (ej: modulo_1): ").strip()

    if id_modulo not in modulos:
        print("Módulo no encontrado.")
        return

    modulo = modulos[id_modulo]
    
    print(f"\nRegistrando notas para el módulo: {modulo['nombre']}")
    
    try:
        nota_teorica = float(input("Nota teórica (0-100): "))
        nota_practica = float(input("Nota práctica (0-100): "))
        nota_quices = float(input("Nota quices/trabajos (0-100): "))
    except ValueError:
        print("Debe ingresar números válidos.")
        return

    # Validar rango
    if not (0 <= nota_teorica <= 100 and 0 <= nota_practica <= 100 and 0 <= nota_quices <= 100):
        print("Las notas deben estar entre 0 y 100.")
        return

    # Cálculo ponderado: 30% teórica, 60% práctica, 10% quices
    nota_final_modulo = (nota_teorica * 0.3) + (nota_practica * 0.6) + (nota_quices * 0.1)

    # Guardar notas en el camper
    if "modulos" not in camper:
        camper["modulos"] = {}
    
    camper["modulos"][id_modulo] = {
        "nombre": modulo["nombre"],
        "nota_teorica": nota_teorica,
        "nota_practica": nota_practica,
        "nota_quices": nota_quices,
        "nota_final": nota_final_modulo,
        "aprobado": nota_final_modulo >= 60
    }

    # Actualizar nota final del camper (promedio de todos los módulos)
    notas_modulos = [mod["nota_final"] for mod in camper["modulos"].values()]
    camper["nota_final"] = sum(notas_modulos) / len(notas_modulos)

    # Actualizar estado de riesgo
    if nota_final_modulo < 60:
        camper["riesgo"] = "Alto"
        print(f"\nALERTA: El camper ha quedado en RIESGO ALTO por nota menor a 60.")
    else:
        camper["riesgo"] = "Bajo"

    guardarDatos(datos)
    
    print(f"\nNotas registradas exitosamente.")
    print(f"Nota final del módulo: {nota_final_modulo:.2f}")
    print(f"Nota final general: {camper['nota_final']:.2f}")
    print(f"{'APROBADO' if nota_final_modulo >= 60 else 'REPROBADO'}")

def ver_notas_camper():
    """Muestra todas las notas de un camper"""
    datos = cargarDatos()

    print("\n--- VER NOTAS DE CAMPER ---")
    
    id_camper = input("Ingrese el ID del camper: ").strip()

    if id_camper not in datos["campers"]:
        print("Camper no encontrado.")
        return

    camper = datos["campers"][id_camper]
    
    print(f"\nCamper: {camper['nombre']} {camper.get('apellidos', '')}")
    print(f"Ruta: {camper.get('ruta_asignada', 'Sin asignar')}")
    print(f"Nota Final General: {camper.get('nota_final', 0):.2f}")
    print(f"Riesgo: {camper.get('riesgo', 'Bajo')}")
    
    modulos = camper.get("modulos", {})
    
    if not modulos:
        print("\nEste camper no tiene notas registradas.")
        return

    print("\nNOTAS POR MÓDULO:")
    print("="*70)
    
    for id_mod, info_mod in modulos.items():
        print(f"\n{info_mod['nombre']}")
        print(f"   Teórica (30%): {info_mod['nota_teorica']:.2f}")
        print(f"   Práctica (60%): {info_mod['nota_practica']:.2f}")
        print(f"   Quices (10%): {info_mod['nota_quices']:.2f}")
        print(f"   NOTA FINAL: {info_mod['nota_final']:.2f}")
        print(f"   Estado: {'APROBADO' if info_mod['aprobado'] else 'REPROBADO'}")

def aprobar_campers():
    """
    Cambia el estado de campers de 'Inscrito' a 'Aprobado'
    después de que hayan pasado la prueba inicial.
    """
    datos = cargarDatos()

    print("\n--- APROBAR CAMPERS ---")
    
    # Mostrar campers inscritos
    campers_inscritos = {id_c: info for id_c, info in datos["campers"].items() 
                         if info["estado"] == "Inscrito"}
    
    if not campers_inscritos:
        print("No hay campers en estado 'Inscrito'.")
        return

    print("\nCampers inscritos:")
    for id_c, info in campers_inscritos.items():
        print(f"  • {id_c} - {info['nombre']} {info.get('apellidos', '')}")

    id_camper = input("\nIngrese el ID del camper a aprobar (o 'todos' para aprobar a todos): ").strip()

    if id_camper.lower() == "todos":
        confirmacion = input(f"⚠️  ¿Aprobar a {len(campers_inscritos)} campers? (s/n): ").strip().lower()
        if confirmacion == "s":
            for id_c in campers_inscritos.keys():
                datos["campers"][id_c]["estado"] = "Aprobado"
            guardarDatos(datos)
            print(f"{len(campers_inscritos)} campers aprobados exitosamente.")
        else:
            print("Operación cancelada.")
        return

    if id_camper not in campers_inscritos:
        print("Camper no encontrado o no está en estado 'Inscrito'.")
        return

    datos["campers"][id_camper]["estado"] = "Aprobado"
    guardarDatos(datos)
    print(f"Camper aprobado exitosamente.")

def ver_campers_en_riesgo():
    """Muestra todos los campers con riesgo alto"""
    datos = cargar_datos()

    print("\n--- CAMPERS EN RIESGO ALTO ---")
    
    campers_riesgo = {id_c: info for id_c, info in datos["campers"].items() 
                      if info.get("riesgo") == "Alto"}
    
    if not campers_riesgo:
        print("No hay campers en riesgo alto.")
        return

    print(f"\nTotal de campers en riesgo: {len(campers_riesgo)}")
    print("="*70)
    
    for id_c, info in campers_riesgo.items():
        print(f"\n{info['nombre']} {info.get('apellidos', '')}")
        print(f"   ID: {id_c}")
        print(f"   Ruta: {info.get('ruta_asignada', 'Sin asignar')}")
        print(f"   Nota Final: {info.get('nota_final', 0):.2f}")
        print(f"   Estado: {info.get('estado')}")
        
        # Mostrar módulos reprobados
        modulos_reprobados = []
        for id_mod, mod_info in info.get("modulos", {}).items():
            if not mod_info.get("aprobado", True):
                modulos_reprobados.append(mod_info["nombre"])
        
        if modulos_reprobados:
            print(f"   Módulos reprobados: {', '.join(modulos_reprobados)}")

def crear_matricula_modulo():
    """
    Crea una matrícula para asignar campers aprobados a un módulo específico
    con trainer, ruta, fechas y salón de entrenamiento.
    """
    datos = cargar_datos()

    print("\n--- CREAR MATRÍCULA DE MÓDULO ---")
    
    # Seleccionar ruta
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
    
    # Seleccionar módulo
    modulos = ruta.get("modulos", {})
    if not modulos:
        print("Esta ruta no tiene módulos.")
        return

    print(f"\nMódulos de la ruta '{nombre_ruta}':")
    for id_mod, info_mod in modulos.items():
        print(f"  • {id_mod}: {info_mod['nombre']}")

    id_modulo = input("\nIngrese el ID del módulo: ").strip()

    if id_modulo not in modulos:
        print("Módulo no encontrado.")
        return

    modulo = modulos[id_modulo]
    
    # Fechas
    fecha_inicio = input("Fecha de inicio (DD/MM/AAAA): ").strip()
    fecha_fin = input("Fecha de finalización (DD/MM/AAAA): ").strip()
    
    modulo["fecha_inicio"] = fecha_inicio
    modulo["fecha_fin"] = fecha_fin

    guardarDatos(datos)
    print(f"\nMatrícula del módulo '{modulo['nombre']}' creada exitosamente.")
    print(f"   Ruta: {nombre_ruta}")
    print(f"   Trainer: {ruta.get('trainer_asignado', 'Sin asignar')}")
    print(f"   Fecha inicio: {fecha_inicio}")
    print(f"   Fecha fin: {fecha_fin}")

def evaluar_rendimiento_ruta():
    """
    Evalúa el rendimiento de cada camper en una ruta.
    Si la nota es menor a 60, el camper queda en riesgo alto.
    """
    datos = cargar_datos()

    print("\n--- EVALUAR RENDIMIENTO DE RUTA ---")
    
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
    campers_ruta = ruta.get("campers_asignados", [])
    
    if not campers_ruta:
        print("No hay campers asignados a esta ruta.")
        return

    print(f"\nEVALUACIÓN DE RENDIMIENTO - RUTA: {nombre_ruta}")
    print("="*70)
    
    campers_bajo_rendimiento = []
    
    for id_camper in campers_ruta:
        if id_camper not in datos["campers"]:
            continue
        
        camper = datos["campers"][id_camper]
        nota_final = camper.get("nota_final", 0)
        
        print(f"\n{camper['nombre']} {camper.get('apellidos', '')}")
        print(f"   Nota Final: {nota_final:.2f}")
        print(f"   Riesgo: {camper.get('riesgo', 'Bajo')}")
        
        if nota_final < 60:
            print(f"   BAJO RENDIMIENTO - Generando llamado de atención")
            campers_bajo_rendimiento.append(camper['nombre'])
            camper["riesgo"] = "Alto"
    
    if campers_bajo_rendimiento:
        print(f"\n{len(campers_bajo_rendimiento)} camper(s) en bajo rendimiento:")
        for nombre in campers_bajo_rendimiento:
            print(f"   • {nombre}")
        guardarDatos(datos)
    else:
        print(f"\nTodos los campers tienen buen rendimiento.")
