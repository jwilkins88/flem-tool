# pylint: disable=abstract-method, missing-module-docstring

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

    is_static = True
    module_name = "Line Module"

    def __init__(self, config: ModuleConfig, width: int, height: int = 1):
        self.__config = config
        self.__width = width
        super().__init__(config, width, height)

    def write(
        self,
        update_device: callable,
        write_queue: callable,
        execute_callback: bool = False,
    ) -> None:
        i = self.__config.position.x
        while i < self.__config.position.x + self.__width:
            write_queue((i, self.__config.position.y, True))
            i += 1

        super().write(update_device, write_queue, execute_callback)
