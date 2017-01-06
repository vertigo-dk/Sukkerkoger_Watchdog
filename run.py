#!/usr/bin/env python
__author__ = 'frederikjuutilainen'

import argparse, threading, time, subprocess, psutil

#receiving osc
from pythonosc import dispatcher
from pythonosc import osc_server

#sending osc
from pythonosc import osc_message_builder
from pythonosc import udp_client

# Main loop / OSC Listener
pi_id = 2
port_in = 7010 + pi_id
port_out = 7001
ip = "localhost"
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
        process_name = "supervisord"
        process_running = False

        for proc in psutil.process_iter():
            if proc.name() == process_name:
                process_running = True
                print('video_player running')

        if(process_running == False):
            print('video_player not running')

        time.sleep(5.0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
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
