# SPDX-FileCopyrightText: Copyright (c) 2020 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import board
import os
import adafruit_sht4x
from microcontroller import watchdog
from watchdog import WatchDogMode

i2c = board.I2C()  # uses board.SCL and board.SDA
sht = adafruit_sht4x.SHT4x(i2c)
# overflow issue with sht41, not present with sht45
# print("Found SHT4x with serial number", hex(sht.serial_number))

sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS

os_info = os.uname()
print(os_info)
ident = f'{{board="{board.board_id}",sysname="{os_info.sysname}",boardname="{os_info.nodename}"}}'

watchdog.mode = WatchDogMode.RESET
watchdog.timeout = 20

while True:
    temperature, relative_humidity = sht.measurements
    print('# BEGIN READOUT')
    print('# TYPE ambient_temperature_celcius gauge')
    print(f'ambient_temperature_celcius{ident} {temperature}')
    print('# TYPE humidity_percent gauge')
    print(f'humidity_percent{ident} {relative_humidity}')
    watchdog.feed()
    time.sleep(5)
