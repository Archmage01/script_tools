# -*- coding: utf-8 -*-
import socket
import sys
import array    # C interface
import time
import struct

sys.path.append('..')

if __name__ == '__main__':
    port = 10506
    ip   = "127.0.0.1"
    dlen = 8
    dly  = 0.4
    if (len(sys.argv) > 4):
        ip = sys.argv[1]
        port = int(sys.argv[2])
        dlen = int(sys.argv[3])
        dly  = float(sys.argv[4])
    elif (len(sys.argv) > 3):
        ip = sys.argv[1]
        port = int(sys.argv[2])
        dlen = int(sys.argv[3])
    elif (len(sys.argv) > 2):
        ip = sys.argv[1]
        port = int(sys.argv[2])
    elif (len(sys.argv) > 1):
        port = int(sys.argv[1])

    #UDP
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    address1 = (ip, port)
    print("Sending... @", ip, port)
    old_a = 1
    xxarr = [i%256 for i in range(0, dlen)]
    cnt = 0
    while 1:
        cnt = cnt + 1
        xxarr[1] = (xxarr[1] + 1)%256
        try:
            arr = bytes(xxarr)
            msg = str('潘磊吃瓜').encode("utf-8")
            print(dlen, len(xxarr), xxarr[0], xxarr[1])
            #s.sendto(arr, ("127.0.0.1",9003))
            s.sendto(msg, ("127.0.0.1",9003))
            time.sleep(dly)
        except socket.timeout:
            print("."),
