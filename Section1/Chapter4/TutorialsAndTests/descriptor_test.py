class CapitalizedValue:
    pass


class Person:
    first_name = CapitalizedValue()
    second_name = CapitalizedValue()

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
