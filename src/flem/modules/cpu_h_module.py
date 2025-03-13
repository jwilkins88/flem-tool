# pylint: disable=abstract-method, missing-module-docstring

from time import sleep
from typing import Callable

import psutil
from loguru import logger

from flem.modules.matrix_module import MatrixModule
from flem.modules.line_module import LineModule
from flem.models.config import ModuleConfig, ModulePositionConfig


class CpuHModule(MatrixModule):
    __line_module: LineModule = None
    __temperature_line_module: LineModule = None
    __config: ModuleConfig = None
    __previous_value: str = "NA"
    __previous_temp: str = "NA"
    __show_temp_argument = "show_temp"
    __temp_sensor_type_argument = "temp_sensor"
    __temp_sensor_index_argument = "temp_sensor_index"
    __show_temp: bool = False

    running = True
    module_name = "CPU Module"

    def __init__(self, config: ModuleConfig = None, width: int = 9, height: int = 12):
        self.__config = config
        header_line_config = ModuleConfig(
            name="header_line",
            position=ModulePositionConfig(x=config.position.x, y=config.position.y + 5),
            refresh_interval=config.refresh_interval,
            module_type="line",
        )

        self.__line_module = LineModule(header_line_config, width)
        self.__show_temp = config.arguments.get(self.__show_temp_argument)
        if self.__show_temp:
            # I'm probably going to use these properties and any calculations associated
            # with them when I start implementing matrix validations
            # self.__height = self.__height + 7
            temperature_line_config = ModuleConfig(
                name="temperature_line",
                position=ModulePositionConfig(
                    x=config.position.x, y=config.position.y + 13
                ),
                refresh_interval=config.refresh_interval,
                module_type="line",
                arguments={"line_style": "dashed"},
            )
            self.__temperature_line_module = LineModule(temperature_line_config, width)
        super().__init__(config, width, height)

    def reset(self):
        """
        Resets the CPU module to its initial state.
        """
        self.__previous_temp = "NA"
        self.__previous_value = "NA"
        return super().reset()

    def write(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
    ) -> None:
        """
        Writes the CPU usage to the matrix display and executes the callback if specified.
        Horizontal style
        """
        try:
            self._write_text(
                "c", write_queue, self.__config.position.y, self.__config.position.x
            )
            self._write_text(
                "p", write_queue, self.__config.position.y, self.__config.position.x + 3
            )
            self._write_text(
                "u", write_queue, self.__config.position.y, self.__config.position.x + 6
            )

            if self.__show_temp:
                self.__temperature_line_module.write(update_device, write_queue, False)

            self.__line_module.write(update_device, write_queue, False)
            while self.running:
                cpu_percentage = str(round(psutil.cpu_percent()))

                cpu_cols = len(cpu_percentage)

                if cpu_cols == 1:
                    cpu_percentage = "0" + cpu_percentage

                start_row = self.__config.position.y + 7
                start_col = self.__config.position.x + 1

                if cpu_percentage == "100":
                    self._write_text("!", write_queue, start_row, start_col)
                else:
                    for i, char in enumerate(cpu_percentage):
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

                if self.__show_temp:
                    start_col = 1
                    sensor_category = psutil.sensors_temperatures().get(
                        self.__config.arguments.get(self.__temp_sensor_type_argument)
                    )
                    target_sensor = sensor_category[
                        self.__config.arguments.get(self.__temp_sensor_index_argument)
                    ]
                    temperature = str(round(target_sensor.current))

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

                self.__previous_value = cpu_percentage
                super().write(update_device, write_queue, execute_callback)
                sleep(self.__config.refresh_interval / 1000)
        except (IndexError, ValueError, TypeError, psutil.Error) as e:
            logger.exception(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)

    def _c(
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
        write_queue((start_col + 2, start_row + 2, False))
        write_queue((start_col + 2, start_row + 3, True))

    def _exclamation(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, True))
        write_queue((start_col, start_row + 4, True))
        write_queue((start_col, start_row + 5, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, True))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, True))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 1, start_row + 5, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))
        write_queue((start_col + 2, start_row + 4, True))
        write_queue((start_col + 2, start_row + 5, True))
