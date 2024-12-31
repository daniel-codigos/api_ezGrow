import meross
import mqtt_info_sen
import time
import asyncio
import os
from crontab import CronTab

credenciales = ["xatak12@gmail.com","enchufamesta99codes"]
info_riego = {"litroHora": "340", "tempWater": "23", "numPausa": "3", "timePausa": "5", "space": "sala22", "sen": "Capacidad", "aparatos": {"bomba": "bomba de agua", "calentador": "calentador agua", "ventilador": "", "oxigenador": "oxigenador"}}
aparatos = [{"regleta": "regleta1", "numChannel": 3, "aparato": "Bomba de agua","space":"sala22"},{"regleta": "regleta1", "numChannel": 2, "aparato": "Calentador agua","space":"sala22"},{"regleta": "regleta2", "numChannel": 1, "aparato": "Oxigenador", "space": "sala22"}]
temp_water = {"topic": "sen_water_temp", "token": "7DGD06VETESC40Y", "name": "Calenta agua", "esp_cat": "sala22"}
capacidad = {"topic": "sen_water_dist", "token": "06AUT2JPL3LFZ8R", "name": "Capacidad", "esp_cat": "sala22"}
comentario = "test_22"


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
                print(info_riego["senTemp"]["state"])
                if info_riego["senTemp"]["state"]:
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
    if temp_water['topic'] == "sen_water_temp" and goCalen:
        temp_task = asyncio.create_task(monitor_temperature(temp_water))

    # Esperar 20 segundos antes de apagar el oxigenador
    await asyncio.sleep(20)

    # Verificar si se debe detener por temperatura o error
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
    mlmin = int(lh) / 60
    min_total = int(info_riego['cantidadRiego']) / mlmin
    minutos = int(min_total)
    minuto_fin = minutos * 60
    segundos = round((min_total - minutos) * 60)
    min_sleep = minuto_fin + segundos
    print("-----------------------------------")
    print(minutos)
    print(segundos)
    print(min_sleep)
    bomba = []
    desague = []
    for cada_aparato in aparatos:
        if cada_aparato['space'] == sala_riego:
            if cada_aparato['aparato'] == "Bomba de agua":
                bomba.append(cada_aparato)
            if cada_aparato['aparato'] == "Desague":
                desague.append(cada_aparato)
    time.sleep(5)
    accion_bomba_on = await meross.main_action(credenciales[0], credenciales[1], {
        "regleta": bomba[0]['regleta'],
        "channel": bomba[0]['numChannel'],
        "aparato": bomba[0]['aparato'],
        "space": sala_riego,
        "accion": "on"
    })
    time.sleep(min_sleep)
    accion_bomba_off = await meross.main_action(credenciales[0], credenciales[1], {
        "regleta": bomba[0]['regleta'],
        "channel": bomba[0]['numChannel'],
        "aparato": bomba[0]['aparato'],
        "space": sala_riego,
        "accion": "off"
    })
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





# if __name__ == "__main__":
#    asyncio.run(lanzarRiego())
#    clean_cron_job(comentario)  # Limpia la entrada del cron después de la ejecución
#    os.remove(__file__)  # Esto elimina el script después de su ejecución

