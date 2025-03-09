# pylint: disable=abstract-method, missing-module-docstring

import json
import subprocess
from time import sleep

from modules.matrix_module import MatrixModule
from modules.line_module import LineModule
from models import ModuleConfig, ModulePositionConfig


class GpuModule(MatrixModule):
    __line_module: LineModule = None
    __width = 3
    __height = 17
    __config: ModuleConfig = None
    __previous_value: str = "NA"

    running = True
    module_name = "GPU Module"

    def __init__(self, config: ModuleConfig = None, width: int = 3, height: int = 17):
        self.__config = config
        self.__width = width
        self.__height = height
        line_config = ModuleConfig(
            position=ModulePositionConfig(x=config.position.x, y=config.position.y + 5),
            refresh_interval=config.refresh_interval,
            module_type="line",
        )
        self.__line_module = LineModule(line_config, self.__width)
        super().__init__(config, width, height)

    def write(
        self,
        update_device: callable,
        write_queue: callable,
        execute_callback: bool = True,
    ) -> None:
        self._write_text(
            "g", write_queue, self.__config.position.y, self.__config.position.x
        )

        self.__line_module.write(update_device, write_queue)
        while self.running:

            gpu_info = json.loads(
                subprocess.check_output(
                    ["/home/joelwilkins/nvtop-dev/usr/local/bin/nvtop", "-s"]
                )
            )
            gpu_percentage = gpu_info[0]["gpu_util"][:-1]

            start_row = self.__config.position.x
            gpu_cols = len(gpu_percentage)

            if gpu_cols == 1:
                gpu_percentage = "0" + gpu_percentage

            start_row = self.__config.position.y + self.__height - 10

            if gpu_percentage == "100":
                self._write_text("!", write_queue, start_row, self.__config.position.x)
            else:
                for i, char in enumerate(gpu_percentage):
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

            self.__previous_value = gpu_percentage
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
