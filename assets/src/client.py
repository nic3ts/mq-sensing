#!/usr/bin/env python

""" client.py - Echo client for sending/receiving C-like structs via socket

References:
- Ctypes fundamental data types: https://docs.python.org/2/library/ctypes.html#ctypes-fundamental-data-types-2
- Ctypes structures: https://docs.python.org/2/library/ctypes.html#structures-and-unions
- Sockets: https://docs.python.org/2/howto/sockets.html
"""

import socket
import sys
import random
from ctypes import *

from mq import *

""" This class defines a C-like struct """
class Payload(Structure):
    _fields_ = [("lpg", c_float),
                ("co", c_float),
                ("smoke", c_float)]


def main():
    server_addr = ('localhost', 2300)
    # server_addr = ('185.244.128.27', 2300)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s < 0:
        print "Error creating socket"

    try:
        s.connect(server_addr)
        print "Connected to %s" % repr(server_addr)
    except:
        print "ERROR: Connection to %s refused" % repr(server_addr)
        sys.exit(1)

    try:
        mq = MQ();
        # for i in range(10):
        while(1):
            print ""
            perc = mq.MQPercentage()
            print("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm\n" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
            time.sleep(0.1)
            payload_out = Payload(perc["GAS_LPG"], perc["CO"], perc["SMOKE"])

            print "Sending LPG=%f ppm, CO=%f, SMOKE=%f" % (payload_out.lpg, payload_out.co, payload_out.smoke)

            nsent = s.send(payload_out)
            # Alternative: s.sendall(...): coontinues to send data until either
            # all data has been sent or an error occurs. No return value.

            print "Sent %d bytes" % nsent

            buff = s.recv(sizeof(Payload))
            payload_in = Payload.from_buffer_copy(buff)
            print "Received LPG=%f ppm, CO=%f, SMOKE=%f" % (payload_in.lpg, payload_in.co, payload_in.smoke)

    finally:
        print "Closing socket"
        s.close()

if __name__ == "__main__":
    main()
