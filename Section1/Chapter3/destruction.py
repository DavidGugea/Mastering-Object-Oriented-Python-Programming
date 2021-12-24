class Noisy:
    def __del__(self) -> None:
        print(f"Removing ${id(self)}")


if __name__ == '__main__':
    ln = [Noisy(), Noisy()]
    del ln # Removing < id > *twice*

    """
    x = Noisy()
    del x # Removing < id > 
    """