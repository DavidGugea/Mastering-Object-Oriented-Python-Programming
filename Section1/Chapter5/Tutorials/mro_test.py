import pprint


class A:
    num = 10
    a = 5


class B(A):
    pass


class C(A):
    num = 1


class D(B, C):
    pass


"""
    A
  /   \
 /     \
B       C
\      /
 \    /
    D
"""

if __name__ == '__main__':
    """
    print(A.__mro__)
    print(B.__mro__)
    print(C.__mro__)
    for cls in D.__mro__:
        print(cls.__name__)
        pprint.pprint(cls.__dict__)
        print("-" * 50)
    """
    print(object.__mro__)
