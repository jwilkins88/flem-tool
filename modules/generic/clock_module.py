# pylint: disable=abstract-method, missing-module-docstring
from datetime import datetime
from time import sleep
from typing import Callable

from modules.matrix_module import MatrixModule
from models import ModuleConfig


class ClockModule(MatrixModule):
    __clock_mode_argument = "clock_mode"
    __clock_modes = ["12h", "24h"]
    __clock_mode = "12h"
    __time_format_12h = "%I%M"
    __time_format_24h = "%H%M"
    __show_seconds_indicator = False
    __show_seconds_indicator_argument = "show_seconds_indicator"
    __config: ModuleConfig = None

    module_name = "Clock Module"

    def __init__(self, config: ModuleConfig, width: int = 9, height: int = 11):
        self.__config = config
        clock_mode = config.arguments.get(self.__clock_mode_argument)
        self.__show_seconds_indicator = config.arguments.get(
            self.__show_seconds_indicator_argument
        )
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
            while self.running:
                time = datetime.now().strftime(
                    self.__time_format_12h
                    if self.__clock_mode == "12h"
                    else self.__time_format_24h
                )

                start_col = 0
                start_row = self.__config.position.y

                for i, char in enumerate(time):
                    if i == 2:
                        start_row += 6
                        start_col = 2
                    elif i == 3:
                        start_col = 6
                    self._write_number(char, write_queue, start_row, start_col)
                    if i < 2:
                        start_col += 4

                if self.__show_seconds_indicator:
                    seconds = int(datetime.now().strftime("%S"))

                    if seconds < 6:
                        write_queue((8, self.__config.position.y, False))
                        write_queue((8, self.__config.position.y + 1, False))
                        write_queue((8, self.__config.position.y + 2, False))
                        write_queue((8, self.__config.position.y + 3, False))
                        write_queue((8, self.__config.position.y + 4, False))
                        write_queue((0, self.__config.position.y + 6, False))
                        write_queue((0, self.__config.position.y + 7, False))
                        write_queue((0, self.__config.position.y + 8, False))
                        write_queue((0, self.__config.position.y + 9, False))
                        write_queue((0, self.__config.position.y + 11, False))
                    if seconds >= 6:
                        write_queue(
                            (
                                8,
                                self.__config.position.y,
                                True if seconds % 2 == 0 else False,
                            )
                        )
                    if seconds >= 12:
                        write_queue(
                            (
                                8,
                                self.__config.position.y + 1,
                                True if seconds % 2 == 0 else False,
                            )
                        )
                    if seconds >= 18:
                        write_queue(
                            (
                                8,
                                self.__config.position.y + 2,
                                True if seconds % 2 == 0 else False,
                            )
                        )
                    if seconds >= 24:
                        write_queue(
                            (
                                8,
                                self.__config.position.y + 3,
                                True if seconds % 2 == 0 else False,
                            )
                        )
                    if seconds >= 30:
                        write_queue(
                            (
                                8,
                                self.__config.position.y + 4,
                                True if seconds % 2 == 0 else False,
                            )
                        )
                    if seconds >= 36:
                        write_queue(
                            (
                                0,
                                self.__config.position.y + 6,
                                True if seconds % 2 == 0 else False,
                            )
                        )
                    if seconds >= 42:
                        write_queue(
                            (
                                0,
                                self.__config.position.y + 7,
                                True if seconds % 2 == 0 else False,
                            )
                        )
                    if seconds >= 48:
                        write_queue(
                            (
                                0,
                                self.__config.position.y + 8,
                                True if seconds % 2 == 0 else False,
                            )
                        )
                    if seconds >= 53:
                        write_queue(
                            (
                                0,
                                self.__config.position.y + 9,
                                True if seconds % 2 == 0 else False,
                            )
                        )
                    if seconds >= 58:
                        write_queue(
                            (
                                0,
                                self.__config.position.y + 10,
                                True if seconds % 2 == 0 else False,
                            )
                        )

                super().write(update_device, write_queue, execute_callback)
                sleep(self.__config.refresh_interval / 1000)
        except (IndexError, ValueError, TypeError) as e:
            print(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)
