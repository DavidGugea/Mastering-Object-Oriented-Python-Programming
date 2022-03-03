import multiprocessing
import time
import logging
import logging.handlers


class LogProducer(multiprocessing.Process):
    handler_class = logging.handlers.QueueHandler


    def __init__(self, proc_id, queue):
        self.proc_id = proc_id
        self.destination = queue
        super().__init__()
        self.log = logging.getLogger(f"{self.__class__.__qualname__}.{self.proc_id}")
        self.log.handlers = [self.handler_class(self.destination)]
        self.log.setLevel(logging.INFO)


    def run(self) -> None:
        self.log.info(f"Started")
        for i in range(100):
            self.log.info(f"Message {i:d}")
            time.sleep(0.001)

        self.log.info(f"Finished")