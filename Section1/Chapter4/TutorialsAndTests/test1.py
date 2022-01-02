def display_dict(x):
    for item in x.items():
        print(item)


class MyClass:
    class_var = 1

    def __init__(self, instance_var):
        self.instance_var = instance_var


if __name__ == '__main__':
    foo = MyClass(2)
    bar = MyClass(3)

    """
    print(foo.class_var)
    print(foo.instance_var)
    print(bar.class_var)
    print(bar.instance_var)
    print(vars(foo))
    print(vars(bar))
    print()
    """

    print(display_dict(MyClass.__class__.__dict__))
    print("-" * 50)
    print(display_dict(MyClass.__dict__))
    print("-" * 50)
    print(MyClass.__bases__)
    print(type(MyClass))
    print(MyClass.__class__)
    print("-" * 50)
    print(display_dict(type.__dict__))
    print("-" * 50)
    print(display_dict(foo.__dict__))

