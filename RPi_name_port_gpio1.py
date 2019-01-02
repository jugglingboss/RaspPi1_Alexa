""" name_port_gpio.py
 
    This is a demo python file showing how to take paramaters
    from command line for device name, port, and GPIO.
    All credit goes to https://github.com/toddmedema/echo/
    for making the first working versions of this code.
"""
 
import fauxmo
import logging
import time
import sys
import RPi.GPIO as GPIO ## Import GPIO library
import subprocess #to run php files
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
 
from debounce_handler import debounce_handler
 
logging.basicConfig(level=logging.DEBUG)
 
class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    #TRIGGERS = {str(sys.argv[1]): int(sys.argv[2])}
    #TRIGGERS = {"office": 52000}
    TRIGGERS = {"ceiling light": 52000,"darkness":51000,"cycle":49000, "sunlight":48000, "blinds down":47000}

    def act(self, client_address, state, name):
        print("State", state, "from client @", client_address)
        # GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
        # GPIO.setup(int(7), GPIO.OUT)   ## Setup GPIO Pin to OUTPUT
        # GPIO.output(int(7), state) ## State is true/false
        if name=="ceiling light":
            subprocess.call(["php", "/var/www/html/LightsOn.php"])
        elif name =="darkness":
            subprocess.call(["php", "/var/www/html/LightsOff.php"])
        elif name =="ice age":
            subprocess.call(["php", "/var/www/html/Air.php"])
        elif name =="cycle":
            subprocess.call(["php", "/var/www/html/BlindsCycle.php"])
        elif name =="sunlight":
            subprocess.call(["php", "/var/www/html/BlindsCycle1.php"])
        elif name =="blinds down":
            subprocess.call(["php", "/var/www/html/BlindsCycle2.php"])
        elif name =="jams":
            subprocess.call(["php", "/var/www/html/PlayMusic.php"])
        elif name =="parties over":
            subprocess.call(["php", "/var/www/html/StopMusic.php"])
        elif name =="power":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "power");
            client.disconnect();
        elif name =="volume up":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "volumeup");
            client.disconnect();
        elif name =="volume ten up":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "volumetenup");
            client.disconnect();
        elif name =="volume down":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "volumedown");
            client.disconnect();
        elif name =="volume ten down":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "volumetendown");
            client.disconnect();
        elif name =="channel up":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "channelup");
            client.disconnect();
        elif name =="channel down":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "channeldown");
            client.disconnect();
        elif name =="up":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "up");
            client.disconnect();
        elif name =="down":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "down");
            client.disconnect();
        elif name =="enter":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "enter");
            client.disconnect();
        elif name =="source":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "source");
            client.disconnect();
        elif name =="up one enter":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "uponeenter");
            client.disconnect();
        elif name =="down one enter":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "downoneenter");
            client.disconnect();
        elif name =="up two enter":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "uptwoenter");
            client.disconnect();
        elif name =="down two enter":
            client = mqtt.Client()
            client.connect("localhost",1883,60)
            client.publish("topic/tv", "downtwoenter");
            client.disconnect();
        else:
            print("Device not found!")




        return True
 
if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)
 
    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)
 
    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            logging.critical("Critical exception: "+ e.args  )
            break
