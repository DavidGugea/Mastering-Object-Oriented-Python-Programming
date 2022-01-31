import sys


def trace(frame, event, arg):
    if frame.f_code.co_name.startswith("__"):
        print(frame.f_code.co_name, frame.f_code.co_filename, event)


sys.settrace(trace)


class noisyfloat(float):
    def __add__(self, other):
        print(self, "+", other)
        return super().__add__(other)

    def __radd__(self, other):
        print(self, "r+", other)
        return super().__radd__(other)

