import pprint


class Meta(type):
    def __new__(cls, class_name, bases, attrs):
        a = {}
        for name, value in attrs.items():
            if name.startswith("__"):
                a[name] = value
            else:
                a[name.upper()] = value

        pprint.pprint(a)

        return type(class_name, bases, a)


class Dog(metaclass=Meta):
    x = 5
    y = 8

    def hello(self) -> None:
        print("hi")


d = Dog()
print(d.X)
