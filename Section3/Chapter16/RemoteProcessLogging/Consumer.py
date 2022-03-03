import collections
import logging
import logging.config
import multiprocessing
import yaml


class LogConsumer(multiprocessing.Process):
    def __init__(self, queue) -> None:
        self.source = queue
        super().__init__()

        logging.config.dictConfig(yaml.load(open("consumer_config.YAML", "r"), Loader=yaml.FullLoader))
        self.combined = logging.getLogger(f"combined.{self.__class__.__qualname__}")
        self.log = logging.getLogger(self.__class__.__qualname__)
        self.counts = collections.Counter()

    def run(self) -> None:
        self.log.info("Consumer Started")
        while True:
            log_record = self.source.get()
            if log_record == None:
                break

            self.combined.handle(log_record)
            self.counts[log_record.getMessage()] += 1

        self.log.info("Consumer Finished")
        self.log.info(self.counts)
