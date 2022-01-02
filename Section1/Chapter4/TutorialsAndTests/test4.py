class Ten:
    def __get__(self, obj, objtype):
        return 10


class A:
    x = 5
    y = Ten()


if __name__ == '__main__':
    a = A()
    print(a.x)
    print(a.y)
