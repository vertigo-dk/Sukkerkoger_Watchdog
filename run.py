#!/usr/bin/env python
__author__ = 'frederikjuutilainen'

import argparse, threading, time

#receiving osc
from pythonosc import dispatcher
from pythonosc import osc_server

#sending osc
from pythonosc import osc_message_builder
from pythonosc import udp_client

# Main loop / OSC Listener
port = 7286
ip = "127.0.0.1"

def quit(unused_addr):
    print('quit')

def shutdown(unused_addr):
    print('shutdown')

def give_status():
    while True:
        print ("Still running")
        time.sleep(1.0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default=ip, help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=port, help="The port to listen on")
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
