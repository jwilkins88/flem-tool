# pylint: disable=abstract-method, missing-module-docstring

import sys
from time import sleep
from typing import Callable
import traceback

import psutil


from modules.matrix_module import MatrixModule
from modules.generic import LineModule
from models import ModuleConfig, ModulePositionConfig


class CpuModule(MatrixModule):
    """
    CpuModule is a subclass of MatrixModule that displays CPU usage on a matrix display.

    Attributes:
        __start_cords (tuple[int, int]): Starting coordinates for the display area.
        __end_cords (tuple[int, int]): Ending coordinates for the display area.
        __line_module (LineModule): An instance of LineModule for additional display functionality.
        running (bool): A flag to control the running state of the module.
        writer_name (str): The name of the writer module.

    Methods:
        __init__(on_bytes: int, off_bytes: int, start_coords: tuple[int, int], \
            end_coords: tuple[int, int]):
            Initializes the CpuModule with the given parameters.

        write(matrix: list[list[int]], callback: callable, execute_callback: bool = True) -> None:
            Writes the CPU usage to the matrix display and executes the callback if specified.

        stop() -> None:
            Stops the CpuModule from running.
    """

    __line_module: LineModule = None
    __config: ModuleConfig = None
    __previous_value: str = "NA"

    running = True
    module_name = "CPU Module"

    def __init__(self, config: ModuleConfig = None, width: int = 3, height: int = 18):
        self.__config = config
        line_config = ModuleConfig(
            name="line",
            position=ModulePositionConfig(x=config.position.x, y=config.position.y + 5),
            refresh_interval=config.refresh_interval,
            module_type="line",
        )
        self.__line_module = LineModule(line_config, self.__width)
        super().__init__(config, width, height)

    def reset(self):
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
                "c", write_queue, self.__config.position.y, self.__config.position.x
            )

            self.__line_module.write(update_device, write_queue, False)
            while self.running:
                cpu_percentage = str(round(psutil.cpu_percent()))

                cpu_cols = len(cpu_percentage)

                if cpu_cols == 1:
                    cpu_percentage = "0" + cpu_percentage

                start_row = self.__config.position.y + 7
                if cpu_percentage == "100":
                    self._write_text(
                        "!", write_queue, start_row, self.__config.position.x
                    )
                else:
                    for i, char in enumerate(cpu_percentage):
                        if char == self.__previous_value[i]:
                            start_row += 6
                            continue

                        self._write_number(
                            char,
                            write_queue,
                            start_row,
                            self.__config.position.x,
                        )
                        start_row += 6

                if self.__previous_value == "100":
                    for i in range(3):
                        write_queue(
                            (
                                self.__config.position.x + i,
                                self.__config.position.y + 12,
                                False,
                            )
                        )

                self.__previous_value = cpu_percentage
                super().write(update_device, write_queue, execute_callback)
                sleep(self.__config.refresh_interval / 1000)
        except (IndexError, ValueError, TypeError, psutil.Error) as e:
            traceback.print_exception(*sys.exc_info())
            print(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)

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
