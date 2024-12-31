import meross
import mqtt_info_sen
import time
import asyncio
import os
from crontab import CronTab

credenciales = ["xatak12@gmail.com","enchufamesta99codes"]
aparatos = [{"regleta": "regleta1", "numChannel": 3, "aparato": "Bomba de agua","space":"sala22"},{"regleta": "regleta1", "numChannel": 2, "aparato": "Calentador agua","space":"sala22"},{"regleta": "regleta2", "numChannel": 1, "aparato": "Oxigenador", "space": "sala22"}]
spacename = 'sala22'
tiempo_rellena = 120



async def lanzarRiego(credenciales, aparatos, spacename, tiempo_rellena):
    cuanto = int(tiempo_rellena) * 1000
    formula = (cuanto / 8000) * 60
    for cada_aparato in aparatos:
        if cada_aparato.aparato == "Bomba de rellenar":
            elegido = cada_aparato
        else:
            break
    print("-----------------------------------")
    sala_riego = spacename
    time.sleep(5)
    accion_bomba_on = await meross.main_action(credenciales[0], credenciales[1], {
        "regleta": elegido['regleta'],
        "channel": elegido['numChannel'],
        "aparato": elegido['aparato'],
        "space": sala_riego,
        "accion": "on"
    })
    time.sleep(formula)
    accion_bomba_off = await meross.main_action(credenciales[0], credenciales[1], {
        "regleta": elegido['regleta'],
        "channel": elegido['numChannel'],
        "aparato": elegido['aparato'],
        "space": sala_riego,
        "accion": "off"
    })
    time.sleep(10)

    print("Proceso completado.")

    #poner bomba desague
    #dormir tiempo restante
    #apagar bomba desague



