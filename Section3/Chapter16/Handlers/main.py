import logging.config
import yaml

config_dict = yaml.load(open("config.YAML", "r"), Loader=yaml.FullLoader)
logging.config.dictConfig(config_dict)

verbose = logging.getLogger("verbose.example.SomeClass")
audit = logging.getLogger("audit.example.SomeClass")

verbose.info("Verbose information")
audit.info("Audit information")