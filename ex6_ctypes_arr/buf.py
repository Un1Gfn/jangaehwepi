#!/usr/bin/env python3

INT_BYTES = 4
INT_BITS = 32
N_NODES = 7

from ctypes import *

print()

# b = create_string_buffer(INT_BYTES*N_NODES)
# print(type(b))
# print(b)
# for i in range(0, N_NODES*INT_BYTES):
#     print(b[i])
# print()

# del b

b = (c_int32 * N_NODES)()
print(type(b))
print(b)
f = CDLL("./buf.so").buf
f.argtypes = [ POINTER(c_int32), c_int32 ]
f(b, N_NODES)
for i in range(0, N_NODES): print(b[i])
print()
