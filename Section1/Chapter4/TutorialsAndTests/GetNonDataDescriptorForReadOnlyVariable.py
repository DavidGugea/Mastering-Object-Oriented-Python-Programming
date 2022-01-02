class ReadOnlyException(Exception):
    def __init__(self, error_msg: str = None) -> None:
        """Raise this exception when a user tries to set a new value to a read-only variable"""
        if error_msg:
            self.error_msg = error_msg
        else:
            self.error_msg = "This variable can't be set to a new value. It's a read only variable"


class ReadOnlyDescriptorNonData:
    def __init__(self, value) -> None:
        self.value = value

    def __get__(self, instance, owner_of_instance) -> None:
        print("Dunder get in descriptor. Instance : {0} || Owner of instance : {1}".format(
            instance,
            owner_of_instance
        ))
        return self.value

    def __set__(self, instance, value) -> None:
        print("Dunder set in descriptor. Instance : {0} || Owner of instance : {1}".format(
            instance,
            value
        ))

        raise ReadOnlyException()


class SomeClass:
    """Some class that will use the ReadOnlyDescriptorNonData descriptor"""
    read_only_variable = ReadOnlyDescriptorNonData()

    def __init__(self, read_only_variable, flexible_variable) -> None:
        self.read_only_variable = ReadOnlyDescriptorNonData(read_only_variable)
        self.flexible_variable = flexible_variable


if __name__ == '__main__':
    x = SomeClass(5, 15)
    print(x.read_only_variable)
