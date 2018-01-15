#!/usr/bin/env python

import sys
import serial
import time

if __name__ == "__main__":
    # 9600, 8N1
    arduino = serial.Serial(
        port = sys.argv[1], # e.g. /dev/ttyACM0 or /dev/ttyUSB0
        baudrate = 9600,
        bytesize=serial.EIGHTBITS,
        stopbits = serial.STOPBITS_ONE,
        parity = serial.PARITY_NONE,
        timeout = 10
    )

    # 9600, 8N1
    hp34401a = serial.Serial(
        port = sys.argv[2], # e.g. /dev/ttyACM0 or /dev/ttyUSB0
        baudrate = 9600,
        bytesize=serial.EIGHTBITS,
        stopbits = serial.STOPBITS_ONE,
        parity = serial.PARITY_NONE,
        timeout = 10
    )

    # the FTDI chip seems to buffer up a certain amount of outgoing bytes if there is no
    # listener to recieve them.  thus, when we first run this script, we will get an initial
    # flood of queued readings.  throw those away.
    then = time.time()
    arduino.readline()
    now = time.time()
    while now - then < 0.2:
        then = time.time()
        arduino.readline()
        now = time.time()

    then = time.time()
    hp34401a.readline()
    now = time.time()
    while now - then < 0.2:
        then = time.time()
        hp34401a.readline()
        now = time.time()

    last_hp_value = None

    oven_out = open("oven-controller.csv", "w")
    tempco_out = open("tempco.csv", "w")
    tempco_out.write("temp_c,ppm,resistance\n")
    tempco_out.flush()

    last_arduino_time = None
    base_r = None

    while True:
        if hp34401a.inWaiting():
            last_hp_value = float(hp34401a.readline().rstrip())
            if base_r is None:
                base_r = last_hp_value
        elif arduino.inWaiting():
            last_arduino_time = time.time()
            if last_hp_value:
                line = arduino.readline()
                oven_out.write(line)
                oven_out.flush()

                c = float(line.rstrip().split(",")[1])
                ppm = (last_hp_value - base_r) / base_r * 1000000.0
                tempco_out.write("%s,%0.2f,%s\n" % (c, ppm, last_hp_value))
                tempco_out.flush()
        else:
            if last_arduino_time is not None and time.time() - last_arduino_time > 1.0:
                oven_out.close()
                tempco_out.close()
                sys.exit(0)

            time.sleep(0.01)
