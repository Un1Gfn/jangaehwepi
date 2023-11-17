#!/usr/bin/env python3

from ctypes import c_int, pointer, byref
from ctypes import CDLL, POINTER
from time import sleep

CONFIG_ENABLE_MANUAL_MODE = False

num = c_int(-1)
pnum = pointer(num)

f = CDLL("./bgtask.so").bgtask
f.argtypes = [POINTER(c_int),]
f(byref(num))

print("please press the <Enter> key with a consistent interval repeatedly")
prev = 0
firstdot = True
while True:
    if CONFIG_ENABLE_MANUAL_MODE:
        input()
    else:
        sleep(0.3)
        print()
    cur = num.value
    if prev == cur:
        if firstdot: print()
        print("   .", end="")
        firstdot = False
    else:
        if firstdot: print()
        print("%4dms" % cur, end="")
        firstdot = True
    prev = cur

