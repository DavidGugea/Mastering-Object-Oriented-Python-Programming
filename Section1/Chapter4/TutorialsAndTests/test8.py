class DataDescriptor:
    def __init__(self, value):
        print("Initialized the data descriptor")
        self.value = value

    def __get__(self, obj, objtype):
        print("Accessed the getter of the descriptor")
        return self.value

    def __set__(self, obj, new_value):
        if new_value < 0:
            raise ValueError("The value can't be less than 0.")

        print("Accessed the setter of the descriptor")
        self.value = new_value


class SomeClass:
    """This is a class that will implement the data descriptor"""
    data_descriptor = DataDescriptor(5)

    def __init__(self, first_number: int, second_number: int) -> None:
        self.first_number = first_number
        self.second_number = second_number

    def get_sum(self) -> int:
        return self.first_number + self.second_number + self.data_descriptor


if __name__ == '__main__':
    x = SomeClass(2, 3)
    print(x.get_sum())
    try:
        x.data_descriptor = -20
    except ValueError:
        x.data_descriptor = 20

    print(x.get_sum())
