try:
    import libcombine
except ImportError:
    import tecombine as libcombine

import sys
from pprint import pprint


time1 = libcombine.OmexDescription.getCurrentDateAndTime()
pprint(sys.modules)
print(type(time1))

print()
print('*' * 80)
print()

import libnuml
pprint(sys.modules)
time2 = libcombine.OmexDescription.getCurrentDateAndTime()
print(type(time2))

del libnuml
time3 = libcombine.OmexDescription.getCurrentDateAndTime()
print(type(time3))

print("end")