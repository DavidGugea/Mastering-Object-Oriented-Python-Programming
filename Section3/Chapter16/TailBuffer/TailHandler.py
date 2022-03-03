import logging.handlers


class TailHandler(logging.handlers.MemoryHandler):
    def shouldFlush(self, record: logging.LogRecord) -> bool:
        """
        Check for buffer full or a record at the flushLevel or higher.
        """

        if record.levelno >= self.flushLevel:
            return True

        while len(self.buffer) > self.capacity:
            self.acquire()
            try:
                del self.buffer[0]
            finally:
                self.release()

            return False