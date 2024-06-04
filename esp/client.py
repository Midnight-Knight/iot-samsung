import machine
import time
import network
import usocket as socket
import ujson as json
import uasyncio as asyncio
import ustruct as struct
from mywebsockets.client import connect
from wifi import do_connect
from buttons import Buttons
from echo import Echo
from sg import Sg90
from water import Water
import _thread
import sys

print("hello world")

tt = False
buttons = False
sg90 = False
echo = False
water = False
led = False
global_websocket = False
timer_listen = 5

async def listen():
    global sg90, global_websocket
    uri = "wss://express-iot.onrender.com:443/iot" # wss://express-iot.onrender.com:443/iot or ws://192.168.1.17:8080/iot
    
    sta_if = network.WLAN(network.STA_IF)
    while not sta_if.isconnected():
        await asyncio.sleep(1)
    try:
        with connect(uri) as websocket:
            print("WebSocket connection established")
            while True:
                try:
                    message = websocket.recv()
                    dataMessage = json.loads(message)
                    print(dataMessage)
                    if dataMessage["message"]["door"] == "unknown" or dataMessage["message"]["door"] == "error":
                        sg90.change(True)
                    else:
                        sg90.change(dataMessage["message"]["door"])
                    if global_websocket == False:
                        global_websocket = websocket
                except Exception as e:
                    print("Error receiving message: ", e)
                    break
    except Exception as e:
        print("WebSocket connection failed: ", e)

def ws_send():
    global echo, water, sg90, global_websocket
    print(f'cm: {echo.cm()}')
    print(f'turbidity: {water.func_water_turbidity()}')
    print(f'water level: {water.func_water_level()}')
    print(f'door: {sg90.get()}')
    data = {
        "message": {
            "door": sg90.get(),
            "food": echo.get(),
            "water": {
                "level": bool(water.func_water_level()),
                "turbidity": water.func_water_turbidity()
            }
        }
    }
    json_str = json.dumps(data)
    if global_websocket != False:
        global_websocket.send(json_str)

def periodic_echo_and_turbidity():
    global timer_listen
    while True:
        ws_send()
        time.sleep(timer_listen)

def periodic_buttons():
    global buttons, timer_listen
    while True:
        if buttons.get_button_1():
            buttons.set_button_1()
            ws_send()
            print("Button 1")
        if buttons.get_button_2():
            buttons.set_button_2()
            timer_listen = 5
            print("Button 2")
        if buttons.get_button_3():
            buttons.set_button_3()
            timer_listen = 30
            print("Button 3")
        if buttons.get_button_4():
            buttons.set_button_4()
            timer_listen = 600
            print("Button 4")
        time.sleep(0.1)

async def periodoc_connect():
    global let
    do_connect(led)

async def main():
    global buttons, sg90, echo, water, tt, led
    led = machine.Pin(2, machine.Pin.OUT)
    await periodoc_connect()

    buttons = Buttons()
    sg90 = Sg90()
    echo = Echo()
    water = Water()

    # Launch periodic tasks
    water.func_water_turbidity()
    thread1 = _thread.start_new_thread(periodic_echo_and_turbidity, ())
    thread2 = _thread.start_new_thread(periodic_buttons, ())
    asyncio.create_task(listen())
    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            tt = True
            sys.exit()

if __name__ == "__main__":
    asyncio.run(main())