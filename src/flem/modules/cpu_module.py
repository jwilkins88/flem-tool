# pylint: disable=abstract-method, missing-module-docstring
from typing import Callable

import psutil
from loguru import logger


from flem.models.config_schema import ModuleSchema
from flem.models.modules.cpu_config import CpuConfig, CpuConfigSchema
from flem.models.modules.line_config import LineConfig, LineConfigArguments
from flem.modules.matrix_module import MatrixModule
from flem.modules.line_module import LineModule
from flem.models.config import ModulePositionConfig


class CpuModule(MatrixModule):
    __line_module: LineModule = None
    __config: CpuConfig = None
    __previous_value: str = "NA"
    __width: int = 3
    __height: int = 18

    running = True
    module_name = "CPU Module"

    def __init__(self, config: CpuConfig = None, width: int = 3, height: int = 18):
        super().__init__(config, width, height)

        if not isinstance(config, CpuConfig):
            self.__config = CpuConfigSchema().load(ModuleSchema().dump(config))
        else:
            self.__config = config

        line_config = LineConfig(
            name="line",
            position=ModulePositionConfig(x=config.position.x, y=config.position.y + 5),
            refresh_interval=config.refresh_interval,
            module_type="line",
            arguments=LineConfigArguments(line_style="solid", width=width),
        )
        self.__line_module = LineModule(line_config, self.__width)

    def start(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
    ):
        self.running = True
        self.reset()
        self.write(update_device, write_queue, execute_callback)

    def stop(self) -> None:
        self.running = False
        return super().stop()

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
        refresh_override: int = None,
        running: bool = True,
    ) -> None:
        """
        Writes the CPU usage to the matrix display and executes the callback if specified.
        """
        try:
            self._write_object(
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

                        self._write_object(
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
                super().write(
                    update_device,
                    write_queue,
                    execute_callback,
                    refresh_override,
                    self.running,
                )
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
        # fmt: off
        char_arr = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        # fmt: on

        self._write_array(char_arr, start_row, start_col, write_queue)
