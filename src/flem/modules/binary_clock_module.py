# pylint: disable=abstract-method, missing-module-docstring
from datetime import datetime
from time import sleep
from typing import Callable

from loguru import logger

from flem.modules.matrix_module import MatrixModule
from flem.models.config import ModuleConfig


class BinaryClockModule(MatrixModule):
    __clock_mode_argument = "clock_mode"
    __clock_modes = ["12h", "24h"]
    __clock_mode = "12h"
    __time_format_12h = "%I%M%S"
    __time_format_24h = "%H%M%S"
    __config: ModuleConfig = None

    module_name = "Binary Clock Module"

    def __init__(self, config: ModuleConfig, width: int = 6, height: int = 4):
        self.__config = config
        clock_mode = config.arguments.get(self.__clock_mode_argument, "12h")
        if clock_mode in self.__clock_modes:
            self.__clock_mode = clock_mode
        super().__init__(config, width, height)

    def write(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
    ) -> None:
        try:
            binary_values = {
                "0": [0, 0, 0, 0],
                "1": [0, 0, 0, 1],
                "2": [0, 0, 1, 0],
                "3": [0, 0, 1, 1],
                "4": [0, 1, 0, 0],
                "5": [0, 1, 0, 1],
                "6": [0, 1, 1, 0],
                "7": [0, 1, 1, 1],
                "8": [1, 0, 0, 0],
                "9": [1, 0, 0, 1],
            }
            while self.running:
                time = datetime.now().strftime(
                    self.__time_format_12h
                    if self.__clock_mode == "12h"
                    else self.__time_format_24h
                )

                for i, char in enumerate(time):
                    for j, value in enumerate(binary_values[char]):
                        write_queue(
                            (
                                self.__config.position.x + i,
                                self.__config.position.y + j,
                                value,
                            )
                        )

                super().write(update_device, write_queue, execute_callback)
        except (IndexError, ValueError, TypeError) as e:
            logger.exception(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)
