import time
import json
import logging


def read_config():
    default_config = {
        "interval": 15,
        "speeds": {
            "0": 15,
            "20": 25,
            "30": 35,
            "40": 55,
            "50": 70,
            "60": 80,
            "70": 95,
            "80": 100,
        },
    }

    try:
        with open("./config.json", "r") as config_file:
            config = json.load(config_file)
            return config
    except:
        logging.warning("config.json not found, using default config")
        with open("./config.json", "w") as config_file:
            json.dump(default_config, config_file, indent=4)
    return default_config


def main():
    logging.info("GPU fan speed controller start.")

    config = read_config()
    interval = config["interval"]
    while True:
        logging.info("Detect")
        time.sleep(interval)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
