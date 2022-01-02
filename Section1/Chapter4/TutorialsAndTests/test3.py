"""
__get__(self, instance, owner) — This will be called when the attribute is retrieved (value = obj.attr), and whatever it returns is what will be given to the code that requested the attribute’s value.
__set__(self, instance, value) — This gets called when a value is set to the attribute (obj.attr = 'value'), and shouldn’t return anything at all.
__delete__(self, instance) — This is called when the attribute is deleted from an object (del obj.attr)
"""

from typing import Dict, Any


def display_dict(dictionary: Dict) -> None:
    for item in dictionary:
        print(item)


class DescriptorClass:
    def __init__(self, initial_value: Any = None, name: str = "var") -> None:
        self.initial_value = initial_value
        self.name = name

    def __get__(self, obj, object_type):
        print("DUNDER GET")
        print(obj)
        print(object_type)
        print("DUNDER GET")

        return self.initial_value

    def __set__(self, obj, value) -> None:
        print("DUNDER SET")
        print(obj)
        print(value)
        print("DUNDER SET")


class SimpleClass:
    x: DescriptorClass = DescriptorClass(1, "variable x")
    y: int = 2


if __name__ == '__main__':
    s = DescriptorClass(5, 'test_variable')
    s.initial_value = 10
