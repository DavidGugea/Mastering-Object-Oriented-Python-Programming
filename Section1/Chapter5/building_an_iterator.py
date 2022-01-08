from collections.abc import Iterator, Container, Sequence

x = [1, 2, 3]
print(iter(x))
x_iter = iter(x)
print(next(x_iter))
print(next(x_iter))
print(next(x_iter))
print(isinstance(x_iter, Iterator))  # True
print(isinstance(x, Iterator))  # False
print(isinstance(x, Container))  # True
print(isinstance(x, Sequence))  # True
