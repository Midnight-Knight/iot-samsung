import machine
import time
import network

ssid = ""
password = ""

def do_connect(led):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            led.value(0)
            time.sleep(1)
            led.value(1)
            time.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())
    led.value(1)