#!/usr/bin/env python
__author__ = 'frederikjuutilainen'

import argparse, threading, time, subprocess

#receiving osc
from pythonosc import dispatcher
from pythonosc import osc_server

#sending osc
from pythonosc import osc_message_builder
from pythonosc import udp_client

# Main loop / OSC Listener
pi_id = 1
port_in = 7010 + pi_id
port_out = 7001
ip = "127.0.0.1"
ip_out = "192.168.1.63"

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
        try:
            # process running
            x = subprocess.check_output(['pidof omxplayer.bin -s'])
            client.send_message("/dead/" + str(pi_id), 0)
            os.system('echo omxplayer running')
        except FileNotFoundError:
            # process not running
            client.send_message("/dead/" + str(pi_id), 1)
            os.system('echo omxplayer not running')

        time.sleep(5.0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default=ip, help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=port_in, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/quit",quit)
    dispatcher.map("/shutdown",shutdown)

    server = osc_server.ThreadingOSCUDPServer(
    (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))

    t = threading.Timer(1.0, give_status)
    t.start()

    server.serve_forever()
