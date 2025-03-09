# pylint: disable=abstract-method, missing-module-docstring

from time import sleep

import psutil

from modules.matrix_module import MatrixModule
from modules.line_module import LineModule
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

    running = True
    module_name = "CPU Module"
    __width = 3
    __height = 17
    __config: ModuleConfig = None

    def __init__(self, config: ModuleConfig = None, width: int = 3, height: int = 17):
        self.__config = config
        self.__width = width
        self.__height = height
        line_config = ModuleConfig(
            position=ModulePositionConfig(x=config.position.x, y=config.position.y + 5),
            refresh_interval=config.refresh_interval,
            module_type="line",
        )
        self.__line_module = LineModule(line_config, width)
        super().__init__(config, width, height)

    def write(
        self,
        update_device: callable,
        write_queue: callable,
        execute_callback: bool = True,
    ) -> None:
        while self.running:
            for i in range(
                self.__config.position.x, self.__config.position.x + self.__width - 1
            ):
                for j in range(
                    self.__config.position.y,
                    self.__config.position.y + self.__height - 1,
                ):
                    write_queue((i, j, False))

            self._write_text(
                "c", write_queue, self.__config.position.y, self.__config.position.x
            )

            self.__line_module.write(update_device, write_queue)
            update_device()
            cpu_percentage = str(round(psutil.cpu_percent()))

            start_row = self.__config.position.x
            # cpu_percentage = "99"
            cpu_cols = len(cpu_percentage)

            if cpu_cols == 1:
                cpu_percentage = "0" + cpu_percentage

            start_row = self.__config.position.y + 17 - 10

            if cpu_percentage == "100":
                self._write_text("!", write_queue, start_row, self.__config.position.x)
            else:
                for char in cpu_percentage:
                    self._write_number(
                        char, write_queue, start_row, self.__config.position.x
                    )
                    start_row += 6

            super().write(update_device, write_queue, execute_callback)
            sleep(self.__config.refresh_interval / 1000)

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
