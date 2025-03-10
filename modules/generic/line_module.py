# pylint: disable=abstract-method, missing-module-docstring
from typing import Callable

from modules.matrix_module import MatrixModule
from models import ModuleConfig


class LineModule(MatrixModule):
    """
    A module for writing a line to a matrix.

    Attributes:
        __start_cords (tuple[int, int]): The starting coordinates of the line.
        __end_cords (tuple[int, int]): The ending coordinates of the line.
        is_static (bool): Indicates if the module is static. Default is True.
        writer_name (str): The name of the writer. Default is "Line Module".

    Methods:
        __init__(on_bytes: int, off_bytes: int, start_coords: tuple[int, int], \
            end_coords: tuple[int, int]):
            Initializes the LineModule with the given parameters.

        write(matrix: list[list[int]], callback: callable, execute_callback: bool = False) -> None:
            Writes a line to the matrix from start_coords to end_coords.
            Calls the callback function if execute_callback is True.
    """

    __line_style_options = ["dashed", "solid"]
    __line_style = "solid"
    __line_style_argument = "line_style"

    is_static = True
    module_name = "Line Module"

    def __init__(self, config: ModuleConfig, width: int = None, height: int = 1):
        self.__config = config
        self.__width = width

        line_style = config.arguments.get(self.__line_style_argument)
        if line_style in self.__line_style_options:
            self.__line_style = line_style
        super().__init__(config, width, height)

    def write(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = False,
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
            print(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)
