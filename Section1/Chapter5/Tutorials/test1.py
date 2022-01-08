import pprint


class Meta(type):
    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        new_class.class_attribute = 10
        return new_class


class Foo(metaclass=Meta):
    pass


if __name__ == '__main__':
    pprint.pprint(Foo.class_attribute)
