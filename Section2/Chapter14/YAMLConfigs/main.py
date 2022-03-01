import yaml

if __name__ == '__main__':
    config = yaml.load(open("config.yaml", "r"))
    print(config)

    simulate(
        config["table"],
        config["player"],
        Path(config["outputfile"])
        config["samples"]
    )