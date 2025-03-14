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
    __use_bar_graph: bool = False
    __use_bar_graph_argument = "use_bar_graph"
    __max_cpu_percentage = 100

    # I might parameterize this, but 100 seems like a reasonable max
    __max_temperature = 100

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

        self.__show_temp = config.arguments.get(self.__show_temp_argument, False)
        self.__use_bar_graph = config.arguments.get(
            self.__use_bar_graph_argument, False
        )

        if self.__show_temp:
            # I'm probably going to use these properties and any calculations associated
            # with them when I start implementing matrix validations
            # self.__height = self.__height + 7
            temperature_line_config = ModuleConfig(
                name="temperature_line",
                position=ModulePositionConfig(
                    x=config.position.x,
                    y=config.position.y + (10 if self.__use_bar_graph else 13),
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
                cpu_percentage = psutil.cpu_percent()
                if self.__use_bar_graph:
                    self._write_cpu_pips(cpu_percentage, write_queue)
                else:
                    self._write_cpu_value(cpu_percentage, write_queue)

                if self.__show_temp:
                    sensor_category = psutil.sensors_temperatures().get(
                        self.__config.arguments.get(self.__temp_sensor_type_argument)
                    )
                    target_sensor = sensor_category[
                        self.__config.arguments.get(self.__temp_sensor_index_argument)
                    ]
                    if self.__use_bar_graph:
                        self._write_temperature_pips(target_sensor.current, write_queue)
                    else:
                        self._write_temperature_value(
                            target_sensor.current,
                            write_queue,
                        )

                super().write(update_device, write_queue, execute_callback)
                sleep(self.__config.refresh_interval / 1000)
        except (IndexError, ValueError, TypeError, psutil.Error) as e:
            logger.exception(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)

    def _write_cpu_pips(
        self,
        cpu_percentage: float,
        write_queue: Callable[[tuple[int, int, bool]], None],
    ):
        start_row = self.__config.position.y + 7
        num_pips = super()._calculate_pips_to_show(
            cpu_percentage, self.__max_cpu_percentage, 18
        )

        col = 0
        for i in range(18):
            pip_on = i <= num_pips
            if i % 2 == 0:
                write_queue((col, start_row, pip_on))
            else:
                write_queue((col, start_row + 1, pip_on))
                col += 1

    def _write_cpu_value(
        self,
        cpu_percentage: float,
        write_queue: Callable[[tuple[int, int, bool]], None],
    ):
        cpu_text = str(round(cpu_percentage))
        cpu_cols = len(cpu_text)

        if cpu_cols == 1:
            cpu_text = "0" + cpu_text

        start_row = self.__config.position.y + 7
        start_col = self.__config.position.x + 1

        if cpu_text == "100":
            self._write_text("!", write_queue, start_row, start_col)
        else:
            for i, char in enumerate(cpu_text):
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

        self.__previous_value = cpu_text

    def _write_temperature_value(
        self,
        cpu_temperature: float,
        write_queue: Callable[[tuple[int, int, bool]], None],
    ):

        start_col = 1
        start_row = self.__config.position.y + 15
        temperature = str(round(cpu_temperature))
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

    def _write_temperature_pips(
        self,
        cpu_temperature: float,
        write_queue: Callable[[tuple[int, int, bool]], None],
    ):
        start_row = self.__config.position.y + 12
        num_pips = super()._calculate_pips_to_show(
            cpu_temperature, self.__max_temperature, 18
        )

        col = 0
        for i in range(18):
            pip_on = i <= num_pips
            if i % 2 == 0:
                write_queue((col, start_row, pip_on))
            else:
                write_queue((col, start_row + 1, pip_on))
                col += 1

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
