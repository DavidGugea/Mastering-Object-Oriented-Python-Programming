class FloatUnits(float):
    def __new__(cls, value, unit):
        obj = super().__new__(cls, float(value))
        obj.unit = unit
        return obj


if __name__ == '__main__':
    speed = FloatUnits(6.8, "testUnit")
    print(speed * 2)
    print(speed.unit)
