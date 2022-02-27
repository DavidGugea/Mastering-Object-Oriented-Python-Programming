import multiprocessing
from Simulate import Simulate


class Simulation(multiprocessing.Process):
    def __init__(
            self,
            setup_queue: multiprocessing.SimpleQueue,
            result_queue: multiprocessing.SimpleQueue
    ) -> None:
        self.setup_queue = setup_queue
        self.result_queue = result_queue
        super().__init__()

    def run(self) -> None:
        """Waits for a termination"""
        print(f"{self.__class__.__name__} start")
        item = self.setup_queue.get()

        while item != (None, None):
            table, player = item
            self.sim = Simulate(table, player, samples=1)
            results = list(self.sim)
            self.result_queue.put((table, player, results[0]))
            item = self.setup_queue.get()

        print(f"{self.__class__.__name__} finish")
