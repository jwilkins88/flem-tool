#!/usr/bin/env python
"""
This module provides functionality for controlling a matrix display using serial communication.
It includes definitions for command values, functions to send commands and render matrices, and
    a main loop to update the display.
Classes:
    CommandVals (IntEnum): Enumeration of command values used for controlling the matrix display.
Functions:
    send_serial(dev, command): Sends a serial command using an existing serial connection.
    send_command(dev, command, parameters=None, with_response=False): Sends a command to the
        specified device.
    send_command_raw(dev, command, with_response=False): Sends a raw command to the device, opening
        a new serial connection each time.
    send_col(dev, s, x, vals): Stages grayscale values for a single column.
    commit_cols(dev, s): Commits the changes from sending individual columns, displaying the matrix.
    render_matrix(dev, matrix): Shows a black/white matrix by sending everything in a single
        command.
    print_matrices(): Prints matrices with a border and specific symbols for matrix values.
    write_columns(device, serial_device, col_vals): Writes column values to a device and commits
        the changes.
    signal_handler(_sig, _frame): Handles the SIGINT signal (Ctrl+C) to gracefully shut down the
    program.
Global Variables:
    RIGHT_DEVICE (str): Path to the right device.
    LEFT_DEVICE (str): Path to the left device.
    WIDTH (int): Width of the matrix.
    HEIGHT (int): Height of the matrix.
    RESPONSE_SIZE (int): Size of the response expected from the device.
    FWK_MAGIC (list): Magic numbers used in commands.
    matrices (dict): Dictionary containing matrices for left, right, and default devices.
    left_matrix (serial.Serial): Serial connection to the left matrix device.
    right_matrix (serial.Serial): Serial connection to the right matrix device.
    ROW (int): Current row being updated in the main loop.
"""

import signal
import os
from time import sleep
import sys

from loguru import logger

from flem.models.config import Config
from flem.utilities.utilities import (
    get_config,
    read_config_from_file,
    has_config_changed,
    run_matrices_from_config,
)
from flem.matrix.matrix import Matrix


def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    for arg in sys.argv:
        if arg == "--debug":
            logger.remove()
            logger.add(sys.stderr, level="DEBUG")

    config: Config
    config_hash: str
    matrices: list[Matrix] = []

    def signal_handler(_sig, _frame):
        """
        Handle the SIGINT signal (Ctrl+C) to gracefully shut down the program.

        This function is called when the user presses Ctrl+C. It performs the following actions:
        1. Prints a message indicating that Ctrl+C was pressed.
        2. Renders the default state of the left and right matrices.
        3. Closes the left and right matrices.
        4. Exits the program with a status code of 0.

        Args:
            sig (int): The signal number.
            frame (FrameType): The current stack frame.
        """
        logger.debug("Ctrl+C pressed. Exiting...")
        for matrix in matrices:
            matrix.stop()

        os._exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    logger.debug("Retrieving configuration...")
    config, config_hash = get_config()

    logger.debug("Running matrices...")
    matrices = run_matrices_from_config(config, matrices)

    # pylint: disable=invalid-name
    any_matrix_running = True
    # pylint: enable=invalid-name

    while any_matrix_running:
        logger.info("Checking if any matrix is running")
        for matrix in matrices:
            logger.info(f"Matrix {matrix.name} is running: {matrix.running}")
            if matrix.running:
                logger.info("At least one matrix is running")
                any_matrix_running = True
                break
            any_matrix_running = False

        logger.info("Checking if configuration has changed")
        config_string = read_config_from_file()

        if has_config_changed(config_hash, config_string):
            logger.info("Configuration has changed. Reloading configuration...")
            config, config_hash = get_config()
            matrices = run_matrices_from_config(config, matrices)

        sleep(10)


if __name__ == "__main__":
    main()
