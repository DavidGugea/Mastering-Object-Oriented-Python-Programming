import numbers
import decimal

print(isinstance(42, numbers.Number))
print(isinstance(355/113, numbers.Number))
print(issubclass(decimal.Decimal, numbers.Number))
print(issubclass(decimal.Decimal, numbers.Integral))
