import asyncio
import os
import time
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.controller.mixins.toggle import ToggleMixin
from meross_iot.model.enums import OnlineStatus
import meross_iot.controller.device as dev_meross
from meross_iot.controller.device import BaseDevice

EMAIL = "xatak12@gmail.com"
PASSWORD = "meneameSta78+!?;"



async def list_dev(email,passwd):
    http_api_client = await MerossHttpClient.async_from_user_password(api_base_url="https://iotx-eu.meross.com",email=email, password=passwd)
    #MerossHttpClient.async_login()
    print("lolasooopatasoooo")
    print(http_api_client.cloud_credentials.to_json())
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()
    await manager.async_device_discovery()

    meross_devices = manager.find_devices()
    print(meross_devices)
    # Print them
    print("I've found the following devices:")
    final_info = []
    for dev in meross_devices:
        #await dev.ChannelInfo(name="cambiatejaja")
        device: BaseDevice = dev
        await device.async_update()
        final_info.append({"name":dev.name,"type":dev.type,"status":str(dev.online_status).replace("<","'").replace(">","'"),"uuid":dev.uuid,"lan_ip":dev.lan_ip})
        #await dev.async_update()
        #print(f"Turning on {dev.name}...")
        #await dev.async_turn_off(channel=2)
    # Close the manager and logout from http_api
    manager.close()
    #await http_api_client.async_logout()
    print(final_info)
    await http_api_client.async_logout()
    return final_info


async def meross_dev_login(email, passwd):
    try:
        # Configura el bucle de eventos
        loop = asyncio.get_event_loop()
        # Configura el cliente HTTP
        http_api_client = await MerossHttpClient.async_from_user_password(api_base_url="https://iotx-eu.meross.com",email=email, password=passwd)
        # Realiza las operaciones que necesitas aquí
        print("lolasooopatasoooo")
        print(http_api_client.cloud_credentials.to_json())
        toda_info = http_api_client.cloud_credentials.to_json()
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()
        manager.close()
        await http_api_client.async_logout()
        return {"Success": True, 'info':toda_info}
    except Exception as e:
        return {"Error": str(e)}


def meross_dev_list(email,passwd):
    try:
        if os.name == 'nt':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(list_dev(email,passwd))
        loop.close()
        #print(result)
        return result
    except Exception as e:
        print(f"Ocurrió una excepción: {str(e)}")
        return {"Error":str(e)}


async def on_enchufe(email,passwd,name,num):
    try:
        http_api_client = await MerossHttpClient.async_from_user_password(api_base_url="https://iotx-eu.meross.com",email=email, password=passwd)
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()
        await manager.async_device_discovery()
        plugs = manager.find_devices(device_name=name)
        if len(plugs) < 1:
            print("No plugs found...")
        else:
            dev = plugs[0]
            await dev.async_update()
            print(f"Turning on {dev.name}...")
            await dev.async_turn_on(channel=num)
            #await dev.async_turn_off(channel=canal)
        manager.close()
        await http_api_client.async_logout()
        return {"Success": True}
    except Exception as e:
        return {"Error": str(e)}


async def off_enchufe(email,passwd,name,num):
    try:
        http_api_client = await MerossHttpClient.async_from_user_password(api_base_url="https://iotx-eu.meross.com",email=email, password=passwd)
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()
        await manager.async_device_discovery()
        plugs = manager.find_devices(device_name=name)
        if len(plugs) < 1:
            print("No plugs found...")
        else:
            dev = plugs[0]
            print("diosito en el final cabron")
            print(plugs)
            await dev.async_update()
            print(f"Turning off {dev.name}...")
            await dev.async_turn_off(channel=num)
        manager.close()
        await http_api_client.async_logout()
        return {"Success": True}
    except Exception as e:
        return {"Error": str(e)}

async def check_status(email,passwd,type_dev):
    try:
        print("loooooooooooooooooooooooooooooooooool")
        http_api_client = await MerossHttpClient.async_from_user_password(api_base_url="https://iotx-eu.meross.com",email=email, password=passwd)
        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()
        await manager.async_device_discovery()
        plugs = manager.find_devices(device_type=type_dev)
        estado = {}
        if len(plugs) < 1:
            print("No plugs found...")
        else:
            dev = plugs
            for cada_regleta in dev:
                await cada_regleta.async_update()
                estado[cada_regleta.name] = []
                for cada_canal in cada_regleta.channels:
                    estado[cada_regleta.name].append({"name":cada_canal.name,"index":cada_canal.index,"status":cada_regleta.is_on(channel=cada_canal.index)})
        manager.close()
        await http_api_client.async_logout()
        return estado
    except Exception as e:
        return {"Error": str(e)}



async def main_login(email,passwd):
    result = await meross_dev_login(email, passwd)
    print("esto es result")
    print(result)
    if result['Success']:
        result_dev = await list_dev(email, passwd)
        print("esto es dev result")
        print(result_dev)
        if "Error" not in result_dev:
            print(result_dev[0]['type'])
            type = result_dev[0]['type']
            #result_togle = await toggle_dev(email,passwd,type,1)
            #print(result_togle)
            status = await check_status(email,passwd,type)
            print(status)
    return result

async def main_action(email,passwd,fin):
    print("okey")
    if fin['accion'] == 'off':
        await off_enchufe(email,passwd,fin['regleta'],fin['channel'])
        returno = {'Succes':'off','regleta':fin['regleta'],'channel':fin['channel']}
    elif fin['accion'] == 'on':
        await on_enchufe(email,passwd,fin['regleta'],fin['channel'])
        returno = {'Succes': 'on','regleta':fin['regleta'],'channel':fin['channel']}
    else:
        returno = {'Error':'Error en accion'}
        print("esto es de broma")
    print(returno)
    return returno

async def main_login2(email,passwd):
    result = await meross_dev_login(email, passwd)
    print(result)
    return result
