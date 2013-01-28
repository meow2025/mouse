#!/usr/bin/env python
from evdev import InputDevice, categorize, ecodes, UInput, list_devices
import time
import os

script_name = 'sample'
dev_name = 'A4TECH USB Device'
dev_phys = 'usb-0000:00:1d.0-1.2/input0'
operations = []


def run(ui):
    for operation in operations:
        if operation['op'] == 'TIME':
            time.sleep(operation['value'] / 1000.0)
        else:
            ui.write(ecodes.EV_KEY, ecodes.ecodes[operation['op']], operation['value'])
            ui.syn()

try:
    path = os.path.split(os.path.realpath(__file__))[0]
    full_script_name = os.path.join(path, script_name)
    with open(full_script_name) as f:
        content = f.read()
        for line in content.split('\n'):
            if line.startswith('#') or len(line) == 0:
                continue
            op, value = line.split(' ')
            operations.append(dict(op=op, value=int(value)))
except IOError:
    print "Can't open", full_script_name
    exit(1)
except:
    print 'Error while processing the script'
    exit(1)

try:
    dev_path = None
    for dev in map(InputDevice, list_devices()):
        if dev.name == dev_name and dev.phys == dev_phys:
            dev_path = dev.fn
    if not dev_path:
        print 'No matching device'
        exit(1)
    dev = InputDevice(dev_path)
    dev.grab()
    ui = UInput()
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY and event.code == ecodes.KEY_LEFTMETA and event.value == 0:
            run(ui)
except OSError, e:
    print 'Please run this script with sudo', e
except KeyboardInterrupt:
    pass
