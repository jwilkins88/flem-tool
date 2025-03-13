# pylint: disable=abstract-method, missing-module-docstring

from time import sleep
from typing import Callable

import psutil
from loguru import logger


from flem.modules.matrix_module import MatrixModule
from flem.modules.line_module import LineModule
from flem.models.config import ModuleConfig, ModulePositionConfig


class CpuModule(MatrixModule):
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
        """
        Resets the CPU module to its initial state.
        This method sets the previous value to "NA" and then calls the reset method
        of the superclass to perform any additional reset operations.
        Returns:
            The result of the superclass reset method.
        """

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
        """
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
            logger.exception(f"Error while running {self.module_name}: {e}")
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
