def my_function(my_parameter: int) -> int:
    return my_parameter + 10


def other_function(other_parameter: str):
    print(other_parameter)

def do_something(param: list[int]):
    pass

other_function(my_function(20))
