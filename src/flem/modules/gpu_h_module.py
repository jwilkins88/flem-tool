# pylint: disable=abstract-method, missing-module-docstring

import json
import subprocess
from time import sleep
from typing import Callable

from loguru import logger

from flem.modules.matrix_module import MatrixModule
from flem.modules.line_module import LineModule
from flem.models.config import ModuleConfig, ModulePositionConfig


class GpuHModule(MatrixModule):
    __line_module: LineModule = None
    __temperature_line_module: LineModule = None
    __width = 9
    __height = 12
    __config: ModuleConfig = None
    __previous_value: str = "NA"
    __previous_temp: str = "NA"
    __gpu_command_argument = "gpu_command"
    __gpu_index_argument = "gpu_index"
    __gpu_command_arguments_argument = "gpu_command_arguments"
    __gpu_util_output_property = "gpu_util_output_property"
    __show_temp_argument = "show_temp"
    __show_temp: bool = False

    running = True
    module_name = "GPU Module"

    def __init__(self, config: ModuleConfig = None, width: int = 9, height: int = 12):
        self.__config = config
        self.__width = width
        self.__height = height
        line_config = ModuleConfig(
            name="line",
            position=ModulePositionConfig(x=config.position.x, y=config.position.y + 5),
            refresh_interval=config.refresh_interval,
            module_type="line",
        )
        self.__line_module = LineModule(line_config, self.__width)
        self.__show_temp = config.arguments.get(self.__show_temp_argument)
        if self.__show_temp:
            self.__height = self.__height + 7
            temperature_line_config = ModuleConfig(
                name="temperature_line",
                position=ModulePositionConfig(
                    x=config.position.x, y=config.position.y + 13
                ),
                refresh_interval=config.refresh_interval,
                module_type="line",
                arguments={"line_style": "dashed"},
            )
            self.__temperature_line_module = LineModule(
                temperature_line_config, self.__width
            )
        super().__init__(config, width, height)

    def reset(self):
        self.__previous_temp = "NA"
        self.__previous_value = "NA"
        return super().reset()

    def write(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
    ) -> None:
        try:
            self._write_text(
                "g", write_queue, self.__config.position.y, self.__config.position.x
            )
            self._write_text(
                "p", write_queue, self.__config.position.y, self.__config.position.x + 3
            )
            self._write_text(
                "u", write_queue, self.__config.position.y, self.__config.position.x + 6
            )

            self.__line_module.write(update_device, write_queue, False)
            while self.running:

                gpu_info = json.loads(
                    subprocess.check_output(
                        [self.__config.arguments[self.__gpu_command_argument]]
                        + self.__config.arguments[
                            self.__gpu_command_arguments_argument
                        ].split(",")
                    )
                )
                gpu_percentage = gpu_info[
                    self.__config.arguments[self.__gpu_index_argument]
                ][self.__config.arguments[self.__gpu_util_output_property]][:-1]

                gpu_cols = len(gpu_percentage)

                if gpu_cols == 1:
                    gpu_percentage = "0" + gpu_percentage

                start_row = self.__config.position.y + 7
                start_col = self.__config.position.x + 1

                if gpu_percentage == "100":
                    self._write_text("!", write_queue, start_row, start_col)
                else:
                    for i, char in enumerate(gpu_percentage):
                        if char == self.__previous_value[i]:
                            start_col += 4
                            continue

                        self._write_number(
                            char,
                            write_queue,
                            start_row,
                            start_col,
                        )
                        start_col += 4

                if self.__previous_value == "100":
                    for i in range(3):
                        write_queue(
                            (
                                self.__config.position.x + i,
                                self.__config.position.y + 12,
                                False,
                            )
                        )

                if self.__show_temp:
                    start_col = 1

                    self.__temperature_line_module.write(
                        update_device, write_queue, False
                    )

                    temperature = gpu_info[
                        self.__config.arguments[self.__gpu_index_argument]
                    ]["temp"][:-1]

                    start_row += 8
                    for i, char in enumerate(temperature):
                        if char == self.__previous_temp[i]:
                            start_col += 4
                            continue

                        self._write_number(
                            char,
                            write_queue,
                            start_row,
                            start_col,
                        )
                        start_col += 4

                    self.__previous_temp = temperature

                if self.__previous_value == "100":
                    for i in range(5):
                        write_queue(
                            (
                                self.__config.position.x + 4,
                                self.__config.position.y + i,
                                False,
                            )
                        )
                        write_queue(
                            (
                                self.__config.position.x + 7,
                                self.__config.position.y + i,
                                False,
                            )
                        )
                        write_queue(
                            (
                                self.__config.position.x + 8,
                                self.__config.position.y + i,
                                False,
                            )
                        )

                self.__previous_value = gpu_percentage
                super().write(update_device, write_queue, execute_callback)
                sleep(self.__config.refresh_interval / 1000)
        except (IndexError, ValueError, TypeError) as e:
            logger.exception(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)

    def _g(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, False))
        write_queue((start_col + 1, start_row + 3, True))
        write_queue((start_col + 2, start_row, False))
        write_queue((start_col + 2, start_row + 1, False))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))

    def _exclamation(
        self, write_queue: callable, start_row: int, start_col: int
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, True))
        write_queue((start_col, start_row + 4, True))
        write_queue((start_col, start_row + 5, True))
        write_queue((start_col, start_row + 6, True))
        write_queue((start_col, start_row + 7, True))
        write_queue((start_col, start_row + 8, True))
        write_queue((start_col, start_row + 9, True))
        write_queue((start_col, start_row + 10, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, True))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, True))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 1, start_row + 5, True))
        write_queue((start_col + 1, start_row + 6, True))
        write_queue((start_col + 1, start_row + 7, True))
        write_queue((start_col + 1, start_row + 8, True))
        write_queue((start_col + 1, start_row + 9, True))
        write_queue((start_col + 1, start_row + 10, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))
        write_queue((start_col + 2, start_row + 4, True))
        write_queue((start_col + 2, start_row + 5, True))
        write_queue((start_col + 2, start_row + 6, True))
        write_queue((start_col + 2, start_row + 7, True))
        write_queue((start_col + 2, start_row + 8, True))
        write_queue((start_col + 2, start_row + 9, True))
        write_queue((start_col + 2, start_row + 10, True))
