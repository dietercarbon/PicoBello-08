#==========================================================================
#
# PB-08-1-10-PicoW_Pub_3_TasterABC_V01.pyw
#
#  3 Taster (Taster A, B, C)
#
#  onboard LED:
#  Z47  *  =  WLAN Verbindung erfolgreich hergestellt
#  Z53  **  =  MQTT-Client erfolgreich erstellt
#  Z61  ***  =  "on" ge-publisht
#
#  Z28  MQTT_TOPIC = "TasterA"
#  Z50  client = MQTTClient("PicoW11", MQTT_BROKER)
#
#==========================================================================
#
# Bibliotheken laden
import machine
import network
from time import sleep
from simple import MQTTClient
from Zugang_DC import wlanSSID, wlanPW, IP_MQTT_broker

# WLAN-Zugangsdaten und MQTT-Broker-Details
WIFI_SSID = wlanSSID()
WIFI_PASSWORD = wlanPW()
MQTT_BROKER = IP_MQTT_broker()
MQTT_TOPIC_A = "TasterA"
MQTT_TOPIC_B = "TasterB"
MQTT_TOPIC_C = "TasterC"

# Initialisieren des Taster-Pins und LED-Anzeige
Button_A = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
Button_B = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
Button_C = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)
LED = machine.Pin("LED", machine.Pin.OUT)

def LED_blinkt(Zahl):
    for Nummer in range(Zahl):
        LED.value(1);sleep(0.3);LED.value(0);sleep(0.2)
    return 

# Verbindung zum WLAN herstellen
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
while not wifi.isconnected():
    sleep(0.1)

Blinki = 1 ;LED_blinkt(Blinki); print("LED_blinkt ", Blinki);sleep(1)
#  *  =  WLAN Verbindung erfolgreich hergestellt

# MQTT-Client erstellen
client = MQTTClient("PicoW11", MQTT_BROKER)

Blinki = 2 ;LED_blinkt(Blinki); print("LED_blinkt ", Blinki);sleep(1)
#  **  =  MQTT-Client erfolgreich erstellt

# Hauptprogramm
while True:
    if Button_A.value() == 0:
        client.connect()
        client.publish(MQTT_TOPIC_A, "Taster A on")
        Blinki = 3 ;LED_blinkt(Blinki); print("LED_blinkt ", Blinki);sleep(1)
        #  ***  =  "on" ge-publisht
        client.disconnect()
        sleep(0.5)
    else:
        sleep(0.1)
        
        
    if Button_B.value() == 0:
        client.connect()
        client.publish(MQTT_TOPIC_B, "Taster B on")
        Blinki = 3 ;LED_blinkt(Blinki); print("LED_blinkt ", Blinki);sleep(1)
        #  ***  =  "on" ge-publisht
        client.disconnect()
        sleep(0.5)
    else:
        sleep(0.1)
        
        
    if Button_C.value() == 0:
        client.connect()
        client.publish(MQTT_TOPIC_C, "Taster C on")
        Blinki = 3 ;LED_blinkt(Blinki); print("LED_blinkt ", Blinki);sleep(1)
        #  ***  =  "on" ge-publisht
        client.disconnect()
        sleep(0.5)
    else:
        sleep(0.1)
        
        



