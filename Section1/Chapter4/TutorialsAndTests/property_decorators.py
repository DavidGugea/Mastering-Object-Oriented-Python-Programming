class Employee:
    def __init__(self, first: str, last: str) -> None:
        self.first = first
        self.last = last

    @property
    def email(self) -> str:
        return "{0}.{1}@email.com".format(self.first, self.last)

    @property
    def fullname(self) -> str:
        return "{0} {1}".format(self.first, self.last)

    @fullname.setter
    def fullname(self, name) -> None:
        self.first, self.last = name.split(" ")

    @fullname.deleter
    def fullname(self) -> None:
        print("Delete Name!")
        self.first = None
        self.last = None


if __name__ == '__main__':
    emp_1 = Employee("John", "Smith")

    emp_1.fullname = "Corey Schafer"
    del emp_1.fullname

    print(emp_1.first)
    print(emp_1.email)
    print(emp_1.fullname)
