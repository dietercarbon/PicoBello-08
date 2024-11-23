#==========================================================================
#
# 20240202 TestPubSub V03.pyw
#
#  1 Taster: button
#  1 LED: LEDext
#
#  onboard LED:
#  Z85    *  =  WLAN Verbindung erfolgreich hergestellt
#  Z101  **  =  Hauptprogramm startet
#  
#
#  
#
#==========================================================================
#
# Bibliotheken laden
import machine
from time import sleep
import network
from simple import MQTTClient
from Zugang_DC import wlanSSID, wlanPW, IP_MQTT_broker

# WLAN-Zugangsdaten und MQTT-Broker-Details
WIFI_SSID = wlanSSID()
WIFI_PASSWORD = wlanPW()
MQTT_BROKER = IP_MQTT_broker()
MQTT_TOPIC_LED = "LED_Control"
MQTT_TOPIC_BUTTON = "Button_State"

# Initialisieren des LED- und Taster-Pins
LEDext = machine.Pin(16, machine.Pin.OUT)
button = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
LED = machine.Pin("LED", machine.Pin.OUT)

# Funktion für Blinki (OnboardLED)
def LED_blinkt(Zahl):
    print("LED_blinkt ", Zahl," x")
    for Nummer in range(Zahl):
        LED.value(1);sleep(0.3);LED.value(0);sleep(0.2)
    return  

# Funktion zum Umschalten der LED
def toggle_LEDext(msg):
    if msg == b"1":
        print("Z46 LED einschalten")
        LEDext.value(1)
    elif msg == b"0":
        print("Z49 LED ausschalten")
        LEDext.value(0)

# Funktion zum Überwachen des Tasterzustands und Veröffentlichen über MQTT
def publish_button_state():
    button_state = button.value()
    message_to_publish = "1" if button_state == 0 else "0"
    
    try:
        client_pub.publish(MQTT_TOPIC_BUTTON, message_to_publish)
        print("Z60 Button State published:", message_to_publish)
    except Exception as e:
        print("Z62 Error publishing Button State:", e)

# Funktion zum Veröffentlichen einer Nachricht über MQTT
def publish_message(topic, message):
    try:
        client_pub.publish(topic, message)
        print("Z68 Message published:", topic, message)
    except Exception as e:
        print("Z70 Error publishing message:", e)

# Funktion, die aufgerufen wird, wenn eine Nachricht empfangen wird
def on_message(topic, msg):
    print("Z74 Message received on topic:", topic, "Message:", msg)
    toggle_LEDext(msg)
    # Hier könnten weitere Aktionen basierend auf der empfangenen Nachricht durchgeführt werden

# Verbindung zum WLAN herstellen
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
while not wifi.isconnected():
    sleep(1)

Blinki = 1 ;LED_blinkt(Blinki)
print("Z86   *  =  WLAN Verbindung erfolgreich hergestellt")

# MQTT-Client erstellen (Provider)
client_pub = MQTTClient("pico_pub", MQTT_BROKER)

# Verbindung zum MQTT-Broker herstellen
client_pub.connect()

# MQTT-Client erstellen (Subscriber)
client_sub = MQTTClient("pico_sub", MQTT_BROKER)
client_sub.set_callback(on_message)
client_sub.connect()
client_sub.subscribe(MQTT_TOPIC_LED)

# Hauptprogramm für den Raspberry Pi Pico
Blinki = 2 ;LED_blinkt(Blinki)
print("Z102   **  =  Hauptprogramm startet ...");print()

try:
    while True:
        # Überwachen Sie den Tasterzustand und veröffentlichen Sie ihn über MQTT
        publish_button_state()
        
        # Überprüfen Sie eingehende MQTT-Nachrichten
        client_sub.check_msg()

        # Hier können Sie weitere spezifische Aktionen für Ihr Programm hinzufügen
        sleep(1)

except KeyboardInterrupt:
    # Beenden Sie das Programm sauber, wenn es durch den Benutzer unterbrochen wird
    print("Programm beendet.")
    client_sub.disconnect()
    client_pub.disconnect()
