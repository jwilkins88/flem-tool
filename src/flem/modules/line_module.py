# pylint: disable=abstract-method, missing-module-docstring
from typing import Callable

from loguru import logger

from flem.modules.matrix_module import MatrixModule
from flem.models.config import ModuleConfig


class LineModule(MatrixModule):
    __line_style_options = ["dashed", "solid"]
    __line_style = "solid"
    __line_style_argument = "line_style"
    __config: ModuleConfig = None
    __width: int = None

    is_static = True
    module_name = "Line Module"

    def __init__(self, config: ModuleConfig, width: int = None, height: int = 1):
        self.__config = config

        line_style = config.arguments.get(self.__line_style_argument)
        if line_style in self.__line_style_options:
            self.__line_style = line_style

        self.__width = width
        super().__init__(config, width, height)

    def write(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
    ) -> None:
        try:
            i = self.__config.position.x
            while i < self.__config.position.x + (
                self.__width or self.__config.arguments["width"]
            ):
                if (
                    self.__line_style == "dashed"
                    and i % 2 == 0
                    or self.__line_style == "solid"
                ):
                    write_queue((i, self.__config.position.y, True))
                i += 1

            super().write(update_device, write_queue, execute_callback)
        except (IndexError, ValueError, TypeError) as e:
            logger.exception(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)
