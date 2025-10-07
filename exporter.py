# pyright: basic
import os
import re
from threading import Thread, Lock
from time import sleep

import serial
from flask import Flask

TTY = os.environ["AMBIENT_USB_TTY"]

app = Flask(__name__)

result_buffer = []
rb_lock = Lock()

class ReadThread(Thread):
    def run(self):
        while True:
            try:
                self._read_port()
            except Exception as e:
                app.logger.error("TTY read error: %s", e, exc_info=e)
                app.logger.info("sleeping 5s then reconnecting")
                sleep(5)

    def _read_port(self):
        try:
            tty = serial.Serial(TTY, timeout=60)
        except Exception as e:
            app.logger.error("cannot connect to TTY: %s", e)

        try:
            while line := tty.readline():
                line = line.decode()
                if re.match(r'^# BEGIN READOUT', line, re.IGNORECASE):
                    with rb_lock:
                        result_buffer.clear()
                else:
                    with rb_lock:
                        result_buffer.append(line)
        finally:
            tty.close()


@app.route("/metrics")
def metrics():
    with rb_lock:
        return "".join(f"{rbl}\n" for rbl in result_buffer)
