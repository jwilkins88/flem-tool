from hashlib import md5
import os
import sys
import traceback

from models import Config, ConfigSchema
from modules import load_module
from led_device import LedDevice
from matrix import Matrix

__CONFIG_PATHS = [f"{os.path.expanduser('~')}/.flem/config.json", "config.json"]


def get_config() -> tuple[Config, str]:
    config_schema: ConfigSchema = ConfigSchema()
    config_string = read_config_from_file()

    return (config_schema.loads(config_string), md5(config_string.encode()).hexdigest())


def read_config_from_file() -> str:
    for path in __CONFIG_PATHS:
        if os.path.exists((path)):
            with open(path, encoding="utf-8") as config_file:
                return config_file.read()

    print("Configuration file not found")
    print("Paths checked: ", end="")
    for path in __CONFIG_PATHS:
        print(f"'{path}", end="")

    raise FileNotFoundError("Configuration file not found")


def has_config_changed(current_config_hash: any, read_config: str) -> bool:
    new_hash = md5(read_config.encode()).hexdigest()
    return current_config_hash != new_hash


def run_matrices_from_config(config: Config, matrices: list[Matrix]) -> list[Matrix]:
    matrices: list[Matrix] = []
    devices: list[LedDevice] = []

    for matrix in matrices:
        matrix[0].stop()
        matrix[1].join(2)

    matrices.clear()

    for device in config.devices:
        device_to_add = LedDevice(device)
        devices.append(device_to_add)

        device_modules = []
        for module in device.modules:
            device_modules.append(load_module(module))

        matrices.append(
            Matrix(
                matrix_device=device_to_add,
                modules=device_modules,
                scenes=device.scenes,
            )
        )

    for matrix in matrices:
        try:
            matrix.run_next_scene()
        except:
            traceback.print_exc(*sys.exc_info())
            print("Something went very wrong starting the modules")

    return matrices
