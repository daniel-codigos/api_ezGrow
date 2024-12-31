import os
from crontab import CronTab
import shutil
# Directorio y archivo a crear


# Código que se escribirá en el archivo
script_code = """#!/usr/bin/env python
import meross
import mqtt_info_sen
import time
import asyncio
import os
from crontab import CronTab

#credenciales
#info_riego
#save_riego
#aparatos
#temp_water
#capacidad
#comentario


async def monitor_temperature(temp_water):
    try:
        cont = 0
        while True:
            # Obtener datos del sensor de manera sincrónica o asíncrona
            temp_sen = mqtt_info_sen.get_info(temp_water['topic'], temp_water['token'])
            respuesta_obtenida = temp_sen.take_info()  # Asegúrate de que esto sea apropiado para tu implementación

            # Chequear la temperatura
            if respuesta_obtenida and 'temperatura' in respuesta_obtenida:
                temp = float(respuesta_obtenida['temperatura'])
                sala_riego = info_riego["space"]
                calentador = []
                for cada_aparato in aparatos:
                    if cada_aparato['space'] == sala_riego:
                        if cada_aparato['aparato'] == "Calentador agua":
                            calentador.append(cada_aparato)
                if temp > info_riego['tempWater']:
                    print(f"Temperatura alta detectada: {temp}°C - Deteniendo el calentador.")
                    accion_calentador_off = await meross.main_action(credenciales[0], credenciales[1], {
                        "regleta": calentador[0]['regleta'],
                        "channel": calentador[0]['numChannel'],
                        "aparato": calentador[0]['aparato'],
                        "space": sala_riego,
                        "accion": "off"
                    })
                    time.sleep(3)
                    return True  # Retorna True para indicar que se debe detener por alta temperatura
                else:
                    print(f"Temperatura actual: {temp}°C")
                    print(f"procedemos a encender el oxigenador")
                    if cont == 0:
                        accion_calentador_on = await meross.main_action(credenciales[0], credenciales[1], {
                                "regleta": calentador[0]['regleta'],
                                "channel": calentador[0]['numChannel'],
                                "aparato": calentador[0]['aparato'],
                                "space": sala_riego,
                                "accion": "on"
                        })
                        cont = cont +1


            await asyncio.sleep(5)  # Pausa de 5 segundos
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return False  # Retorna False para indicar un error
def clean_cron_job(comentario_del):
    from crontab import CronTab
    cron = CronTab(user=True)
    # Busca y elimina el job por su comentario
    cron.remove_all(comment=comentario_del)
    cron.write()
async def lanzarRiego():
    #15minutos de oxi y ventilador si hay
    # fin = {"regleta":master,"name":name,"channel":numChannel,'accion':accion,'space':espacioName}
    # Encender oxigenador
    # Encender ventilador agua
    goOxi = False
    goCalen = False
    sala_riego = info_riego["space"]
    oxigenador = []
    for cada_aparato in aparatos:
        if cada_aparato['space'] == sala_riego:
            if cada_aparato['aparato'] == "Oxigenador":
                print("oxiiiiiiiiii")
                print(cada_aparato)
                oxigenador.append(cada_aparato)
                goOxi = True
            if cada_aparato['aparato'] == "Calentador agua":
                print(save_riego["senTemp"]["state"])
                if save_riego["senTemp"]["state"]:
                    goCalen = True
    time.sleep(5)
    if goOxi:
        accion_oxi_on = await meross.main_action(credenciales[0], credenciales[1], {
            "regleta": oxigenador[0]['regleta'],
            "channel": oxigenador[0]['numChannel'],
            "aparato": oxigenador[0]['aparato'],
            "space": sala_riego,
            "accion": "on"
        })

    # Iniciar la tarea de monitoreo de temperatura en segundo plano
    if temp_water != None:
        if temp_water['topic'] == "sen_water_temp" and goCalen:
            temp_task = asyncio.create_task(monitor_temperature(temp_water))

    # Esperar 20 segundos antes de apagar el oxigenador
    await asyncio.sleep(20)

    # Verificar si se debe detener por temperatura o error
    if temp_water != None:
        if temp_water['topic'] == "sen_water_temp" and goCalen:
            if await temp_task:
                print("Deteniendo otras operaciones por seguridad.")
        else:
            # Apagar oxigenador
            time.sleep(5)
    if goOxi:
        accion_oxi_off = await meross.main_action(credenciales[0], credenciales[1], {
                "regleta": oxigenador[0]['regleta'],
                "channel": oxigenador[0]['numChannel'],
                "aparato": oxigenador[0]['aparato'],
                "space": sala_riego,
                "accion": "off"
        })
    print("Oxigenador apagado correctamente.")
    lh = info_riego["litroHora"]
    print(lh)
    ml_h_bomba = int(lh) * 1000
    mlmin = ml_h_bomba / 60
    min_total = int(info_riego['cantidadRiego']) / mlmin
    minutos = int(min_total)
    minuto_fin = minutos * 60
    segundos = round((min_total - minutos) * 60)
    min_riego_total = minuto_fin + segundos
    print("-----------------------------------")
    print(minutos)
    print(segundos)
    print(min_riego_total)
    cada_sleep_riego_tiempo = min_riego_total / int(save_riego['numPausa'])
    lapausica = int(save_riego['timePausa']) * 60
    print('dormimos riego')
    print(cada_sleep_riego_tiempo)
    bomba = []
    desague = []
    for cada_aparato in aparatos:
        if cada_aparato['space'] == sala_riego:
            if cada_aparato['aparato'] == "Bomba de riego":
                bomba.append(cada_aparato)
            if cada_aparato['aparato'] == "Desague":
                desague.append(cada_aparato)
    time.sleep(5)
    print("empezamos el riego!!")
    for cada_vuelta in range(0,int(save_riego['numPausa'])):
        accion_bomba_on = await meross.main_action(credenciales[0], credenciales[1], {
            "regleta": bomba[0]['regleta'],
            "channel": bomba[0]['numChannel'],
            "aparato": bomba[0]['aparato'],
            "space": sala_riego,
            "accion": "on"
        })
        time.sleep(cada_sleep_riego_tiempo)
        accion_bomba_off = await meross.main_action(credenciales[0], credenciales[1], {
            "regleta": bomba[0]['regleta'],
            "channel": bomba[0]['numChannel'],
            "aparato": bomba[0]['aparato'],
            "space": sala_riego,
            "accion": "off"
        })
        time.sleep(lapausica)
        
    print("Proceso completado.")
    time.sleep(10)
    act_desague_on = await meross.main_action(credenciales[0], credenciales[1], {
        "regleta": desague[0]['regleta'],
        "channel": desague[0]['numChannel'],
        "aparato": desague[0]['aparato'],
        "space": sala_riego,
        "accion": "on"
    })
    time.sleep(120)
    act_desague_off = await meross.main_action(credenciales[0], credenciales[1], {
        "regleta": desague[0]['regleta'],
        "channel": desague[0]['numChannel'],
        "aparato": desague[0]['aparato'],
        "space": sala_riego,
        "accion": "off"
    })
    print("Proceso completado.")
    #poner bomba desague
    #dormir tiempo restante
    #apagar bomba desague





if __name__ == "__main__":
    asyncio.run(lanzarRiego())
    clean_cron_job(comentario)  # Limpia la entrada del cron después de la ejecución
    os.remove(__file__) 

"""



def crear_archivos(archivo,hora,datos,script):
    target_directory = "/home/pi/proyecto_porta/auth/users/riegos"
    # Cambiar a la carpeta objetivo
    if not os.path.exists(target_directory):
        print(f"La carpeta '{target_directory}' no existe. Creándola...")
        os.makedirs(target_directory)
    os.chdir(target_directory)
    print("Cambiado a la carpeta:", target_directory)
    # Comprobar si existe la carpeta 'user'
    if not os.path.exists(datos[0][2]):
        print("La carpeta 'user' no existe. Creándola...")
        os.makedirs(datos[0][2])

    # Cambiar a la carpeta 'user'
    print(f"Cambiando a la carpeta: {datos[0][2]}")
    os.chdir(datos[0][2])

    # Ruta de los archivos originales
    archivo1 = '/home/pi/proyecto_porta/auth/users/lanzamos/mqtt_info_sen.py'
    archivo2 = '/home/pi/proyecto_porta/auth/users/lanzamos/meross.py'

    # Copiar los archivos a la nueva carpeta
    try:
        shutil.copy(archivo1, datos[0][2])
        shutil.copy(archivo2, datos[0][2])
        print("Archivos copiados exitosamente.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    print("Ubicación actual en la carpeta 'user':", os.getcwd())
    ubic = os.getcwd()+"/"+archivo+".py"
    script = script.replace("#credenciales", "credenciales = "+str(datos[0]))
    script = script.replace("#info_riego", "info_riego = " + str(datos[1]))
    script = script.replace("#save_riego", "save_riego = " + str(datos[6]))
    script = script.replace("#aparatos", "aparatos = " + str(datos[2]).replace("<QuerySet ","").replace(">",""))
    script = script.replace("#temp_water", "temp_water = " + str(datos[3]))
    script = script.replace("#capacidad", "capacidad = " + str(datos[4]))
    script = script.replace("#comentario", "comentario = '" + archivo + "'")
    # Paso 2: Crear el archivo y escribir el código
    with open(ubic, 'w') as file:
        file.write(script)
    # Paso 3: Asignar permisos de ejecución
    os.chmod(os.getcwd(), 0o755)

    # Paso 4: Configurar crontab
    cron = CronTab(user=True)
    hora_l, minuto = hora.split(":")
    jobs = list(cron.find_comment(archivo))
    if not jobs:
        job = cron.new(command=f'python3 {ubic}', comment=archivo)
        job.setall(f'{minuto} {hora_l} * * *')  # Ejecuta según la hora proporcionada
        cron.write()
        print(f"Nueva tarea cron creada para {archivo}.")
    else:
        print(f"Ya existe una tarea cron con el comentario '{archivo}'.")

    print(f"Archivo creado y programado para ejecutarse: {ubic}")


'''
if __name__ == "__main__":
    credenciales = ["pololo","xatak12@gmail.com", "enchufamesta99codes"]
    info_riego = {"litroHora": "4000", "tempWater": 23, "likidoTotal": "-6.07", "cantidadRiego": "250",
                  "horaRiegoStr": "10:25", "fertis": "noFertis", "space": "sala22"}
    aparatos = [{"regleta": "regleta1", "numChannel": 3, "aparato": "Bomba de agua", "space": "sala22"},
                {"regleta": "regleta1", "numChannel": 2, "aparato": "Calentador agua", "space": "sala22"},
                {"regleta": "regleta2", "numChannel": 1, "aparato": "Oxigenador", "space": "sala22"}]
    temp_water = {"topic": "sen_water_temp", "token": "7DGD06VETESC40Y", "name": "Calenta agua", "esp_cat": "sala22"}
    capacidad = {"topic": "sen_water_dist", "token": "06AUT2JPL3LFZ8R", "name": "Capacidad", "esp_cat": "sala22"}
    comentario = "test_22"
    #riego_user_hora_diaHoy
    #riego_pololo_14_1205
    #14:00
    datos = [credenciales,info_riego,aparatos,temp_water,capacidad,"riego_pololo_14_1205"]
    crear_archivos("riego_pololo_14_1205","14:00",datos,script_code)
#archivo,hora,datos
#datos:
#credenciales
#info_riego
#aparatos
#temp_water
#capacidad
#comentario'''