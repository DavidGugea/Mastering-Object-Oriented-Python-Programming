from typing import List, Any


class Test(list):
    def __getitem__(self, item) -> Any:
        print(item)
        print(item.start)
        print(item.stop)
        print(item.step)
        print(item.indices(3))
        return super().__getitem__(item)


if __name__ == '__main__':
    x = Test(list(range(0, 11)))
    print(x[0:5:2])