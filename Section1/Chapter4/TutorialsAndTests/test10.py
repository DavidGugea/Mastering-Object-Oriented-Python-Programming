def function(a, *, b, c) -> int:
    print(a + b + c)


if __name__ == '__main__':
    function(1, 2, 3)