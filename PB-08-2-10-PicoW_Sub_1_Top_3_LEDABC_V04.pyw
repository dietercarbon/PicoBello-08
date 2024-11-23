#==========================================================================
#
# PB-08-2-10-PicoW_Sub_1_Top_3_LEDABC_V04.pyw
#
#  3 LEDs A, B, C 
#
#  onboard LED:
#  Z47  *  =  WLAN Verbindung erfolgreich hergestellt
#  Z53  **  =  MQTT-Client erfolgreich erstellt
#  Z69  ***  =  mit MQTT verbunden und warten im Hauptprogramm
#
#  Z28  MQTT_TOPIC = "TasterA"
#  Z50  client = MQTTClient("PicoW21", MQTT_BROKER)
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
MQTT_TOPIC = "LEDs"
#MQTT_TOPIC_A = "LEDgr_A"
#MQTT_TOPIC_B = "LEDge_B"
#MQTT_TOPIC_C = "LEDro_C"

# Initialisieren des Relais-Pins
LEDgr_Relais_A = machine.Pin(20, machine.Pin.OUT)
LEDge_Relais_B = machine.Pin(19, machine.Pin.OUT)
LEDro_Relais_C = machine.Pin(18, machine.Pin.OUT)
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
client = MQTTClient("PicoW08", MQTT_BROKER)

Blinki = 2 ;LED_blinkt(Blinki); print("LED_blinkt ", Blinki);sleep(1)
#  **  =  MQTT-Client erfolgreich erstellt


# Funktion zum Umschalten des Relais
def toggle_relay(topic, msg):
    #msg_str = msg.decode('utf-8')
    if msg  == b"1":
        print (msg)
        LEDgr_Relais_A.value(1)
    elif msg == b"2":
        print (msg)
        LEDgr_Relais_A.value(0)
        
    if msg == b"3":
        print (msg)
        LEDge_Relais_B.value(1)
    elif msg == b"4":
        print (msg)
        LEDge_Relais_B.value(0)
        
    if msg == b"5":
        print (msg)
        LEDro_Relais_C.value(1)
    elif msg == b"6":
        print (msg)
        LEDro_Relais_C.value(0)


# MQTT-Abonnent erstellen und verbinden
client.set_callback(toggle_relay)
client.connect()
client.subscribe(MQTT_TOPIC)
#client.subscribe(MQTT_TOPIC_A)

Blinki = 3 ;LED_blinkt(Blinki); print("LED_blinkt ", Blinki);sleep(1)
 #  ***  =  mit MQTT verbunden und warten im Hauptprogramm

# Hauptprogramm - auf Nachrichten warten
while True:
    client.wait_msg()
    
