from hashlib import md5
import os
import sys
import traceback

from loguru import logger

from models import Config, ConfigSchema
from modules import load_module
from led_device import LedDevice
from matrix import Matrix

__CONFIG_PATHS = [f"{os.path.expanduser('~')}/.flem/config.json", "config.json"]


def get_config() -> tuple[Config, str]:
    """
    Reads a configuration file, parses it into a Config object, and returns the
    Config object along with the MD5 hash of the configuration string.
    Returns:
        tuple[Config, str]: A tuple containing the parsed Config object and the
        MD5 hash of the configuration string.
    """
    config_schema: ConfigSchema = ConfigSchema()
    config_string = read_config_from_file()

    return (config_schema.loads(config_string), md5(config_string.encode()).hexdigest())


def read_config_from_file() -> str:
    """
    Reads the configuration from the first available file in the predefined configuration paths.
    This function iterates over a list of predefined configuration file paths and returns the content
    of the first file it finds. If no configuration file is found, it prints an error message and raises
    a FileNotFoundError.
    Returns:
        str: The content of the configuration file.
    Raises:
        FileNotFoundError: If no configuration file is found in the predefined paths.
    """

    for path in __CONFIG_PATHS:
        logger.debug(f"Checking for configuration file at '{path}'")
        if os.path.exists((path)):
            logger.debug(f"Reading configuration from '{path}'")
            with open(path, encoding="utf-8") as config_file:
                return config_file.read()

    logger.error("Configuration file not found")
    raise FileNotFoundError("Configuration file not found")


def has_config_changed(current_config_hash: any, read_config: str) -> bool:
    """
    Checks if the configuration has changed by comparing the current configuration hash
    with the hash of the provided configuration string.
    Args:
        current_config_hash (any): The hash of the current configuration.
        read_config (str): The configuration string to compare against.
    Returns:
        bool: True if the configuration has changed, False otherwise.
    """

    new_hash = md5(read_config.encode()).hexdigest()
    logger.debug(f"Current config hash: {current_config_hash}, new hash: {new_hash}")
    return current_config_hash != new_hash


def run_matrices_from_config(config: Config, matrices: list[Matrix]) -> list[Matrix]:
    """
    Initializes and runs matrices based on the provided configuration.
    This function stops and clears any existing matrices, initializes new matrices
    based on the devices specified in the configuration, and runs the next scene
    for each matrix.
    Args:
        config (Config): The configuration object containing device information.
        matrices (list[Matrix]): A list of Matrix objects to be initialized and run.
    Returns:
        list[Matrix]: A list of initialized and running Matrix objects.
    """

    devices: list[LedDevice] = []

    logger.debug("Stopping and clearing existing matrices")
    for matrix in matrices:
        logger.debug(f"Stopping matrix {matrix.name}")
        matrix.stop()

    logger.debug("Clearing matrix list")
    matrices.clear()

    for device in config.devices:
        logger.debug(f"Adding device {device.name}")
        device_to_add = LedDevice(device)
        devices.append(device_to_add)

        device_modules = []
        logger.debug("Loading modules")
        for module in device.modules:
            logger.debug(f"Loading module {module.name}")
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
            logger.info(f"Running matrix {matrix.name}")
            matrix.run_next_scene()
        except (RuntimeError, TypeError, NameError) as e:
            logger.exception(f"Error while running matrix {matrix.name}: {e}")

    return matrices
