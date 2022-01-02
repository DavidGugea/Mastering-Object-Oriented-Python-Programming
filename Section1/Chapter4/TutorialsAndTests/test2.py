class MyClass:
    class_variable: int = 1

    def __init__(self, instance_variable: int) -> None:
        self.instance_variable = instance_variable


if __name__ == '__main__':
    foo = MyClass(2)
    print(foo.class_variable)
    MyClass.class_variable = 5
    print(foo.class_variable)
    print(foo.__dict__)
    print(MyClass.__dict__)