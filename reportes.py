# reportes.py
from UTILS.init import cargarDatos

def menu_reportes():
    """
    Menú de reportes del sistema.
    Incluye todos los reportes solicitados en el proyecto.
    """
    while True:
        print("\n" + "-"*50)
        print("MÓDULO DE REPORTES DEL SISTEMA")
        print("-"*50)
        print("1. Listar campers inscritos")
        print("2. Listar campers que aprobaron el examen inicial")
        print("3. Listar trainers trabajando con CampusLands")
        print("4. Listar campers con bajo rendimiento")
        print("5. Listar campers y trainers por ruta")
        print("6. Mostrar módulos perdidos/aprobados por ruta")
        print("7. Reporte completo del sistema")
        print("8. Volver al menú principal")
        print("-"*50)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            listar_campers_inscritos()
        elif opcion == "2":
            listar_campers_aprobados()
        elif opcion == "3":
            listar_trainers()
        elif opcion == "4":
            listar_campers_bajo_rendimiento()
        elif opcion == "5":
            listar_campers_trainers_por_ruta()
        elif opcion == "6":
            mostrar_modulos_por_ruta()
        elif opcion == "7":
            reporte_completo()
        elif opcion == "8":
            break
        else:
            print("Opción inválida.")

def listar_campers_inscritos():
    """Lista todos los campers que están en estado 'Inscrito'"""
    datos = cargarDatos()

    print("\n" + "="*70)
    print("REPORTE: CAMPERS INSCRITOS")
    print("="*70)

    campers_inscritos = {id_c: info for id_c, info in datos["campers"].items() 
                         if info["estado"] == "Inscrito"}

    if not campers_inscritos:
        print("No hay campers en estado 'Inscrito'.")
        return

    print(f"\nTotal: {len(campers_inscritos)} campers")
    print("-"*70)

    for id_c, info in campers_inscritos.items():
        print(f"\nID: {id_c}")
        print(f"   Nombre: {info['nombre']} {info.get('apellidos', '')}")
        print(f"   Dirección: {info['direccion']}")
        print(f"   Acudiente: {info['acudiente']}")
        print(f"   Teléfono: {info.get('telefono_celular', 'N/A')}")

def listar_campers_aprobados():
    """Lista todos los campers que aprobaron el examen inicial"""
    datos = cargarDatos()

    print("\n" + "="*70)
    print("REPORTE: CAMPERS QUE APROBARON EL EXAMEN INICIAL")
    print("="*70)

    campers_aprobados = {id_c: info for id_c, info in datos["campers"].items() 
                         if info["estado"] in ["Aprobado", "Cursando", "Graduado"]}

    if not campers_aprobados:
        print("No hay campers que hayan aprobado el examen inicial.")
        return

    print(f"\nTotal: {len(campers_aprobados)} campers")
    print("-"*70)

    for id_c, info in campers_aprobados.items():
        print(f"\nID: {id_c}")
        print(f"   Nombre: {info['nombre']} {info.get('apellidos', '')}")
        print(f"   Estado actual: {info['estado']}")
        print(f"   Ruta asignada: {info.get('ruta_asignada', 'Sin asignar')}")

def listar_trainers():
    """Lista todos los trainers que están trabajando con CampusLands"""
    datos = cargarDatos()

    print("\n" + "="*70)
    print("REPORTE: TRAINERS DE CAMPUSLANDS")
    print("="*70)

    if not datos["trainers"]:
        print("No hay trainers registrados.")
        return

    print(f"\nTotal: {len(datos['trainers'])} trainers")
    print("-"*70)

    for id_t, info in datos["trainers"].items():
        print(f"\nID: {id_t}")
        print(f"   Nombre: {info['nombre']}")
        print(f"   Horario: {info['horario']['inicio']}:00 - {info['horario']['fin']}:00")
        print(f"   Especialidades: {', '.join(info['especialidades'])}")
        print(f"   Rutas asignadas: {len(info.get('rutas_asignadas', []))}")
        if info.get('rutas_asignadas'):
            print(f"   → {', '.join(info['rutas_asignadas'])}")
        print(f"   Disponible: {'Sí' if info.get('disponible', True) else 'No'}")

def listar_campers_bajo_rendimiento():
    """Lista campers que cuentan con bajo rendimiento (riesgo alto)"""
    datos = cargarDatos()

    print("\n" + "="*70)
    print("REPORTE: CAMPERS CON BAJO RENDIMIENTO")
    print("="*70)

    campers_bajo_rendimiento = {id_c: info for id_c, info in datos["campers"].items() 
                                if info.get("riesgo") == "Alto"}

    if not campers_bajo_rendimiento:
        print("No hay campers con bajo rendimiento.")
        return

    print(f"\nTotal: {len(campers_bajo_rendimiento)} campers")
    print("-"*70)

    for id_c, info in campers_bajo_rendimiento.items():
        print(f"\nID: {id_c}")
        print(f"   Nombre: {info['nombre']} {info.get('apellidos', '')}")
        print(f"   Ruta: {info.get('ruta_asignada', 'Sin asignar')}")
        print(f"   Nota Final: {info.get('nota_final', 0):.2f}")
        print(f"   Estado: {info['estado']}")
        print(f"   Riesgo: {info['riesgo']}")
        
        # Módulos reprobados
        modulos_reprobados = []
        for id_mod, mod_info in info.get("modulos", {}).items():
            if not mod_info.get("aprobado", True):
                modulos_reprobados.append(f"{mod_info['nombre']} ({mod_info['nota_final']:.2f})")
        
        if modulos_reprobados:
            print(f"   Módulos reprobados:")
            for mod in modulos_reprobados:
                print(f"      • {mod}")

def listar_campers_trainers_por_ruta():
    """Lista campers y trainers que se encuentran asociados a cada ruta"""
    datos = cargarDatos()

    print("\n" + "="*70)
    print("REPORTE: CAMPERS Y TRAINERS POR RUTA")
    print("="*70)

    if not datos["rutas"]:
        print("No hay rutas registradas.")
        return

    for nombre_ruta, info_ruta in datos["rutas"].items():
        print(f"\nRUTA: {nombre_ruta}")
        print("="*70)
        
        # Trainer
        trainer_id = info_ruta.get("trainer_asignado")
        if trainer_id and trainer_id in datos["trainers"]:
            trainer = datos["trainers"][trainer_id]
            print(f"\nTRAINER:")
            print(f"   • {trainer['nombre']} (ID: {trainer_id})")
            print(f"   • Horario: {trainer['horario']['inicio']}:00 - {trainer['horario']['fin']}:00")
        else:
            print(f"\nTRAINER: Sin asignar")
        
        # Campers
        campers_ruta = info_ruta.get("campers_asignados", [])
        print(f"\nCAMPERS ({len(campers_ruta)}/{info_ruta['capacidad']}):")
        
        if not campers_ruta:
            print("   • No hay campers asignados")
        else:
            for id_camper in campers_ruta:
                if id_camper in datos["campers"]:
                    camper = datos["campers"][id_camper]
                    nota = camper.get("nota_final", 0)
                    print(f"   • {camper['nombre']} {camper.get('apellidos', '')} (ID: {id_camper})")
                    print(f"     Estado: {camper['estado']} | Nota: {nota:.2f} | Riesgo: {camper.get('riesgo', 'Bajo')}")
        
        print("-"*70)

def mostrar_modulos_por_ruta():
    """
    Muestra cuántos campers perdieron y aprobaron cada uno de los módulos
    teniendo en cuenta la ruta de entrenamiento y el trainer encargado.
    """
    datos = cargarDatos()

    print("\n" + "="*70)
    print("REPORTE: MÓDULOS PERDIDOS Y APROBADOS POR RUTA")
    print("="*70)

    if not datos["rutas"]:
        print("No hay rutas registradas.")
        return

    for nombre_ruta, info_ruta in datos["rutas"].items():
        print(f"\nRUTA: {nombre_ruta}")
        print(f"Trainer: {info_ruta.get('trainer_asignado', 'Sin asignar')}")
        print("="*70)
        
        modulos = info_ruta.get("modulos", {})
        campers_ruta = info_ruta.get("campers_asignados", [])
        
        if not modulos:
            print("No hay módulos en esta ruta.")
            continue
        
        if not campers_ruta:
            print("No hay campers asignados a esta ruta.")
            continue
        
        # Analizar cada módulo
        for id_mod, info_mod in modulos.items():
            print(f"\nMódulo: {info_mod['nombre']}")
            
            aprobados = 0
            reprobados = 0
            sin_calificar = 0
            
            # Contar estadísticas
            for id_camper in campers_ruta:
                if id_camper not in datos["campers"]:
                    continue
                
                camper = datos["campers"][id_camper]
                modulos_camper = camper.get("modulos", {})
                
                if id_mod in modulos_camper:
                    if modulos_camper[id_mod].get("aprobado", False):
                        aprobados += 1
                    else:
                        reprobados += 1
                else:
                    sin_calificar += 1
            
            # Mostrar estadísticas
            total_evaluados = aprobados + reprobados
            print(f"   Aprobados: {aprobados}")
            print(f"   Reprobados: {reprobados}")
            print(f"   ⏳ Sin calificar: {sin_calificar}")
            
            if total_evaluados > 0:
                porcentaje_aprobacion = (aprobados / total_evaluados) * 100
                print(f"   Tasa de aprobación: {porcentaje_aprobacion:.1f}%")
        
        print("-"*70)

def reporte_completo():
    """Genera un reporte completo del sistema"""
    datos = cargarDatos()

    print("\n" + "="*70)
    print("REPORTE COMPLETO DEL SISTEMA CAMPUSLANDS")
    print("="*70)

    # Estadísticas generales
    total_campers = len(datos["campers"])
    total_trainers = len(datos["trainers"])
    total_rutas = len(datos["rutas"])

    print(f"\nESTADÍSTICAS GENERALES:")
    print(f"   Total Campers: {total_campers}")
    print(f"   Total Trainers: {total_trainers}")
    print(f"   Total Rutas: {total_rutas}")

    # Campers por estado
    print(f"\nCAMPERS POR ESTADO:")
    estados = {}
    for camper in datos["campers"].values():
        estado = camper["estado"]
        estados[estado] = estados.get(estado, 0) + 1
    
    for estado, cantidad in estados.items():
        porcentaje = (cantidad / total_campers * 100) if total_campers > 0 else 0
        print(f"   • {estado}: {cantidad} ({porcentaje:.1f}%)")

    # Campers por riesgo
    print(f"\nCAMPERS POR NIVEL DE RIESGO:")
    riesgos = {}
    for camper in datos["campers"].values():
        riesgo = camper.get("riesgo", "Bajo")
        riesgos[riesgo] = riesgos.get(riesgo, 0) + 1
    
    for riesgo, cantidad in riesgos.items():
        porcentaje = (cantidad / total_campers * 100) if total_campers > 0 else 0
        print(f"   • {riesgo}: {cantidad} ({porcentaje:.1f}%)")

    # Distribución por rutas
    print(f"\nDISTRIBUCIÓN POR RUTAS:")
    for nombre_ruta, info_ruta in datos["rutas"].items():
        num_campers = len(info_ruta.get("campers_asignados", []))
        capacidad = info_ruta["capacidad"]
        ocupacion = (num_campers / capacidad * 100) if capacidad > 0 else 0
        print(f"   • {nombre_ruta}: {num_campers}/{capacidad} ({ocupacion:.1f}% ocupación)")

    # Trainers y su carga
    print(f"\nCARGA DE TRAINERS:")
    for id_t, info_t in datos["trainers"].items():
        num_rutas = len(info_t.get("rutas_asignadas", []))
        print(f"   • {info_t['nombre']}: {num_rutas} ruta(s) asignada(s)")

    # Promedio general
    if total_campers > 0:
        notas = [c.get("nota_final", 0) for c in datos["campers"].values() if c.get("nota_final", 0) > 0]
        if notas:
            promedio_general = sum(notas) / len(notas)
            print(f"\nPROMEDIO GENERAL: {promedio_general:.2f}")
        else:
            print(f"\nPROMEDIO GENERAL: No hay notas registradas")

    print("\n" + "="*70)
