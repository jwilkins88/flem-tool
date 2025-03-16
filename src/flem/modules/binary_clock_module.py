# pylint: disable=abstract-method, missing-module-docstring
from datetime import datetime
from typing import Callable

from loguru import logger

from flem.models.config_schema import ModuleSchema
from flem.models.modules.clock_config import ClockConfig, ClockConfigSchema
from flem.modules.matrix_module import MatrixModule


class BinaryClockModule(MatrixModule):
    __time_format_12h = "%I%M%S"
    __time_format_24h = "%H%M%S"
    __config: ClockConfig = None
    __binary_values = {
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

    module_name = "Binary Clock Module"

    def __init__(self, config: ClockConfig, width: int = 6, height: int = 4):
        super().__init__(config, width, height)

        if not isinstance(config, ClockConfig):
            self.__config = ClockConfigSchema().load(ModuleSchema().dump(config))
        else:
            self.__config = config

    def stop(self) -> None:
        self.running = False
        return super().stop()

    def write(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
        refresh_override: int = None,
    ) -> None:
        try:
            while self.running:
                time = datetime.now().strftime(
                    self.__time_format_12h
                    if self.__config.arguments.clock_mode == "12h"
                    else self.__time_format_24h
                )

                for i, char in enumerate(time):
                    for j, value in enumerate(self.__binary_values[char]):
                        write_queue(
                            (
                                self.__config.position.x + i,
                                self.__config.position.y + j,
                                value,
                            )
                        )

                super().write(
                    update_device, write_queue, execute_callback, refresh_override
                )
        except (IndexError, ValueError, TypeError) as e:
            logger.exception(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)
