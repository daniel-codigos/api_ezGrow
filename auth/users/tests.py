credenciales = ['xatak12@gmail.com', 'enchufamesta99codes', 'pololo']
info_riego = {'litroHora': '162', 'tempWater': '23', 'likidoTotal': '3.52', 'cantidadRiego': '10000', 'horaRiegoStr': '15:00', 'fertis': 'noFertis', 'space': 'sala22'}
save_riego = {'litroHora': '162', 'tempWater': '23', 'numPausa': '3', 'timePausa': '5', 'space': 'sala22', 'senCap': {'name': 'sen_water_dist', 'state': False}, 'senTemp': {'name': 'sen_water_dist', 'state': False}, 'aparatos': {'bomba': 'bomba de riego', 'bombaRellena': 'bomba de rellenar', 'calentador': 'calentador agua', 'ventilador': '', 'oxigenador': 'oxigenador'}}
aparatos = [{'regleta': 'regleta1', 'numChannel': 1, 'aparato': 'Lampara', 'space': 'sala22'}, {'regleta': 'regleta1', 'numChannel': 3, 'aparato': 'Extractor', 'space': 'sala22'}, {'regleta': 'regleta1', 'numChannel': 4, 'aparato': 'Ventilador', 'space': 'sala22'}, {'regleta': 'regleta1', 'numChannel': 5, 'aparato': 'Sensores', 'space': 'sala22'}, {'regleta': 'abajo1', 'numChannel': 1, 'aparato': 'Lampara', 'space': 'sala22'}, {'regleta': 'abajo1', 'numChannel': 4, 'aparato': 'Bomba de riego', 'space': 'sala22'}, {'regleta': 'abajo1', 'numChannel': 3, 'aparato': 'Calentador agua', 'space': 'sala22'}, {'regleta': 'abajo1', 'numChannel': 2, 'aparato': 'Oxigenador', 'space': 'sala22'}, {'regleta': 'abajo2', 'numChannel': 1, 'aparato': 'Bomba de rellenar', 'space': 'sala22'}]
temp_water = None
capacidad = {'topic': 'sen_water_dist', 'token': 'IOI8TEWSYQZ3TJF', 'name': 'Capacidd agua', 'esp_cat': 'sala22'}
comentario = 'riego_pololo_15_47'

print("Oxigenador apagado correctamente.")
lh = info_riego["litroHora"]
print(lh)
ml_h_bomba = int(lh) * 1000
mlmin = ml_h_bomba / 60
print(mlmin)
print(int(info_riego['cantidadRiego']))
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
print(float(cada_sleep_riego_tiempo))
print(lapausica)
bomba = []
desague = []

