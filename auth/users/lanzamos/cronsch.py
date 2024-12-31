import schedule
import datetime
import time

# Variable para controlar la ejecución del bucle
continuar_ejecucion = True

def ejecutar_tarea(user_id):
    global continuar_ejecucion
    print("Tarea ejecutada a las:", datetime.datetime.now(), "para el usuario ID:", user_id)
    # Simular una condición de "registro completado"
    continuar_ejecucion = False

def programar_tarea_a_hora(hora, user_id):
    ahora = datetime.datetime.now()
    hora_objetivo = ahora.replace(hour=hora, minute=0, second=0, microsecond=0)

    if ahora >= hora_objetivo:
        hora_objetivo += datetime.timedelta(days=1)

    schedule.every().day.at(hora_objetivo.strftime("%H:%M")).do(ejecutar_tarea, user_id).tag('tarea_unico_dia')
    print(f"Tarea programada para {hora_objetivo}, para el usuario ID: {user_id}")

def mostrar_tareas_pendientes():
    print("Tareas cron pendientes:")
    for job in schedule.jobs:
        print(job)

def cancelar_tareas():
    schedule.clear('tarea_unico_dia')

# Ejemplo de uso
hora_programada = 17
user_id = 12345
programar_tarea_a_hora(hora_programada, user_id)

try:
    while continuar_ejecucion:
        mostrar_tareas_pendientes()
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa detenido por el usuario.")
finally:
    mostrar_tareas_pendientes()
    cancelar_tareas()
    print("Programa terminado.")
