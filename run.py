#!/usr/bin/env python3
__author__ = 'frederikjuutilainen'

import argparse, threading, time, subprocess, psutil, socket, serial

#receiving osc
from pythonosc import dispatcher
from pythonosc import osc_server

#sending osc
from pythonosc import osc_message_builder
from pythonosc import udp_client

# Main loop / OSC Listener
pi_hostname = socket.gethostname()
pi_hostname_array = pi_hostname.split('-')
pi_id = int(pi_hostname_array[-1])
port_in = 7010 + pi_id
port_out = 7001
ip = socket.gethostname() # IP of pi ('localhost' isn't enough)
ip_out = "glycomics.local"

# setup serial out for screen remote control
ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

#    ser.write(('Write counter: %d \n'%(counter)).encode('utf-8'))
def setVol(unused_addr, args):
    vol = args[0]
#    ser.write(0xAAFE120100+vol)
    ser.write(0xAA)
    ser.write(0xFE)
    ser.write(0x01)
    ser.write(vol)

def screenTurnOn(unused_addr):
#    ser.write(0xAAFE110101)
    ser.write(0xAA)
    ser.write(0xFE)
    ser.write(0x01)
    ser.write(0x01)

def screenTurnOff(unused_addr):
#    ser.write(0xAAFE110100)
    ser.write(0xAA)
    ser.write(0xFE)
    ser.write(0x01)
    ser.write(0x00)

def shutdown(unused_addr):
    import os
    os.system('echo shutting down')
    os.system("sudo shutdown -h now")

def give_status():
    import os
# Check processes running and send /ok if video player is running
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=ip_out,
    help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=port_out,
    help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)

    # check processes running
    while True:
        process_name = "omxplayer"
        process_running = False

        for proc in psutil.process_iter():
            if proc.name() == process_name:
                process_running = True
                client.send_message("/dead/" + str(pi_id), 0)

        if(process_running == False):
            client.send_message("/dead/" + str(pi_id), 1)

        time.sleep(5.0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default=ip, help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=port_in, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()

    dispatcher.map("/setVol",setVol)
    dispatcher.map("/screenTurnOn",screenTurnOn)
    dispatcher.map("/screenTurnOff",screenTurnOff)

    dispatcher.map("/quit",quit)
    dispatcher.map("/shutdown",shutdown)

    server = osc_server.ThreadingOSCUDPServer(
    (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))

    t = threading.Timer(1.0, give_status)
    t.start()

    server.serve_forever()
