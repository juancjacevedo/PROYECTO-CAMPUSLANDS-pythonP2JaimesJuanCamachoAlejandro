
import os
import json

try:
    from trainers import cargarDatos
except Exception:
    def cargarDatos(arg, path=None):
       
        if isinstance(arg, str) and path is None:
            file_path = arg
            if not os.path.isabs(file_path):
                file_path = os.path.join(os.getcwd(), file_path)
            if not os.path.exists(file_path):
                return []
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except Exception:
                    return []

        if path and isinstance(path, str):
            file_path = path
            if not os.path.isabs(file_path):
                file_path = os.path.join(os.getcwd(), file_path)
            data = []
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except Exception:
                        data = []

            
            if isinstance(arg, dict) and "id" in arg:
                updated = False
                for i, item in enumerate(data):
                    if isinstance(item, dict) and item.get("id") == arg["id"]:
                        data[i] = arg
                        updated = True
                        break
                if not updated:
                    data.append(arg)
            else:
                
                data = arg

            os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True

        raise ValueError("Invalid arguments to cargarDatos")


campers = cargarDatos("data/campers.json")
trainers = cargarDatos("data/trainers.json")


def campersAsignadosTrainer(idTrainer):
    found_id = next((t["id"] for t in trainers if t.get("id") == idTrainer), None)
    if not found_id:
        print("Trainer no encontrado")
        return []
    return [c for c in campers if c.get("idTrainer") == found_id]


def listarCampersTrainer(id_trainer):
    campers_asignados = campersAsignadosTrainer(id_trainer)
    if not campers_asignados:
        print("No hay campers asignados a este trainer")
        return
    print("--- Campers asignados ---")
    for c in campers_asignados:
        print(f"ID: {c.get('id')} | Nombre: {c.get('nombres')} {c.get('apellidos')} | Estado: {c.get('estado')}")


def registrarNotas(idTrainer):
    asignados = campersAsignadosTrainer(idTrainer)
    if not asignados:
        print("No tiene campers asignados")
        return

    listarCampersTrainer(idTrainer)
    idCamper = input("Ingrese ID del camper a evaluar: ").strip()
    camper = next((c for c in asignados if c.get("id") == idCamper), None)
    if not camper:
        print("Camper no encontrado o no asignado a tus rutas")
        return

    modulo = input("Nombre del módulo: ").strip()
    try:
        notaTeo = float(input("Nota teórica (0-100): "))
        notaPrac = float(input("Nota práctica (0-100): "))
        notaQuiz = float(input("Nota quizes/trabajos (0-100): "))
    except Exception:
        print("Entrada inválida")
        return

    nota_final = round(notaTeo * 0.3 + notaPrac * 0.6 + notaQuiz * 0.1, 2)

    if "historial_modulos" not in camper or not isinstance(camper["historial_modulos"], list):
        camper["historial_modulos"] = []
    camper["historial_modulos"].append({"modulo": modulo, "nota_final": nota_final})
    camper["riesgo"] = "Alto" if nota_final < 60 else "Bajo"

    
    cargarDatos(camper, "data/campers.json")
    print(f"Nota registrada para {camper.get('nombres')} {camper.get('apellidos')} - Nota final: {nota_final}")


def actualizarNotas(idTrainer):
    asignados = campersAsignadosTrainer(idTrainer)
    if not asignados:
        print("No tiene campers asignados")
        return

    print("--- RENDIMIENTO DE CAMPERS ---")
    for c in asignados:
        if not c.get("historial_modulos"):
            print(f"{c.get('nombres')} {c.get('apellidos')}: Sin evaluaciones")
        else:
            promedio = sum([m.get("nota_final", 0) for m in c.get("historial_modulos", [])]) / len(c.get("historial_modulos", []))
            print(f"{c.get('nombres')} {c.get('apellidos')}: Promedio: {promedio:.2f} | Riesgo: {c.get('riesgo')}")


def menuTrainer():
    while True:
        print("--- MENÚ TRAINER ---")
        print("1. Ver campers asignados")
        print("2. Registrar notas")
        print("3. Actualizar notas")
        print("4. Volver")

        opcion = input("Seleccione: ").strip()

        if opcion == "1":
            listarCampersTrainer(input("Ingrese ID del trainer: ").strip())
        elif opcion == "2":
            registrarNotas(input("Ingrese ID del trainer: ").strip())
        elif opcion == "3":
            actualizarNotas(input("Ingrese ID del trainer: ").strip())
        elif opcion == "4":
            break
        else:
            print("Opción inválida")
