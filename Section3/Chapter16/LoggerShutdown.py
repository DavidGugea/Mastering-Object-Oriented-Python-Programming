import sys
import yaml
import logging

if __name__ == '__main__':
    logging.config.dictConfig(yaml.load("log_config.yaml"))

    try:
        application = Main()
        status = application.run()
    except Exception as e:
        logging.exception(e)
        status = 1
    finally:
        logging.shutdown()

    sys.exit(status)