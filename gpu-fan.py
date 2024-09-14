import time
import json
import logging

import pynvml


def read_config():
    default_config = {
        "interval": 15,
        "speeds": {
            "0": 30,
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


def to_list(speeds: dict):
    speeds = [(temp, speed) for (temp, speed) in speeds.items()]
    return sorted(speeds, key=lambda s: s[0], reverse=True)


def update_fan_speed(idx, speeds: dict):
    handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
    gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, 0)
    gpu_speed = pynvml.nvmlDeviceGetFanSpeed(handle)

    target_speed = 30
    for temp, speed in speeds:
        if gpu_temp >= int(temp):
            target_speed = speed
            break

    logging.info(f"GPU{idx}: {gpu_temp} °C")
    if gpu_speed != target_speed:
        fan_count = pynvml.nvmlDeviceGetNumFans(handle)
        pynvml.nvmlDeviceSetFanSpeed_v2(handle, 0, target_speed)
        logging.info(f"Set fan of GPU{idx} to {target_speed}%")


def main():
    logging.info("GPU fan speed controller start.")

    config = read_config()
    interval = config["interval"]
    speeds = to_list(config["speeds"])
    try:
        pynvml.nvmlInit()
    except:
        logging.error("Cannot initialize nvml.")
        exit(1)

    device_count = pynvml.nvmlDeviceGetCount()
    try:
        while True:
            for device in range(device_count):
                update_fan_speed(device, speeds)
            time.sleep(interval)
    except Exception as e:
        logging.error(e)
    finally:
        # set to default policy
        for device in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(device)
            pynvml.nvmlDeviceSetFanControlPolicy(handle, 0, 0)
        pynvml.nvmlShutdown()


if __name__ == "__main__":
    log_format = "%(asctime)s - [%(levelname)s] %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)
    main()
