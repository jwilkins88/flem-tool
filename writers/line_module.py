# pylint: disable=abstract-method, missing-module-docstring

from writers.matrix_module import MatrixModule


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

    __start_cords: tuple[int, int] = None
    __end_cords: tuple[int, int] = None

    is_static = True
    writer_name = "Line Module"

    def __init__(
        self,
        on_bytes: int,
        off_bytes: int,
        start_coords: tuple[int, int],
        end_coords: tuple[int, int],
    ):
        super().__init__(on_bytes, off_bytes)
        self.__start_cords = start_coords
        self.__end_cords = end_coords

    def write(
        self,
        matrix: list[list[int]],
        callback: callable,
        execute_callback: bool = False,
    ) -> None:
        i = self.__start_cords[0]
        while i < self.__end_cords[0]:
            matrix[i][self.__start_cords[1]] = self._on
            i += 1

        super().write(matrix, callback, execute_callback)
