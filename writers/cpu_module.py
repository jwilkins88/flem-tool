# pylint: disable=abstract-method, missing-module-docstring

from time import sleep

import psutil

from writers.matrix_module import MatrixModule
from writers.line_module import LineModule


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

        _exclamation(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Draws an exclamation mark on the matrix display.

        _blink(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for blinking functionality.

        _c(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the character 'C'.

        _eight(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the number '8'.

        _five(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the number '5'.

        _four(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the number '4'.

        _g(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the character 'G'.

        _nine(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the number '9'.

        _one(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the number '1'.

        _percent(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the percent symbol '%'.

        _seven(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the number '7'.

        _six(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the number '6'.

        _three(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the number '3'.

        _two(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the number '2'.

        _zero(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Placeholder method for drawing the number '0'.
    """

    __start_cords: tuple[int, int] = None
    __end_cords: tuple[int, int] = None
    __line_module: LineModule = None

    running = True
    writer_name = "CPU Module"

    def __init__(
        self,
        on_bytes: int,
        off_bytes: int,
        start_coords: tuple[int, int],
        end_coords: tuple[int, int],
    ):
        super().__init__(on_bytes, off_bytes)
        self.writer_name = "CPU Module"
        self.__start_cords = start_coords
        self.__end_cords = end_coords
        self.__line_module = LineModule(
            on_bytes,
            off_bytes,
            (start_coords[0], start_coords[1] + 6),
            (start_coords[0] + 3, start_coords[1] + 6),
        )

    def write(
        self, matrix: list[list[int]], callback: callable, execute_callback: bool = True
    ) -> None:
        while self.running:
            for i in range(self.__start_cords[0], self.__end_cords[0]):
                for j in range(self.__start_cords[1], self.__end_cords[1]):
                    matrix[i][j] = self._off

            self._write_text("c", matrix, self.__start_cords[1], self.__start_cords[0])
            self.__line_module.write(matrix, callback)

            cpu_percentage = str(round(psutil.cpu_percent()))

            start_row = self.__start_cords[0]
            # cpu_percentage = "99"
            cpu_cols = len(cpu_percentage)

            if cpu_cols == 1:
                cpu_percentage = "0" + cpu_percentage

            start_row = self.__end_cords[1] - 10

            if cpu_percentage == "100":
                self._write_text("!", matrix, start_row, self.__start_cords[0])
            else:
                for char in cpu_percentage:
                    self._write_number(char, matrix, start_row, self.__start_cords[0])
                    start_row += 6

            super().write(matrix, callback, execute_callback)
            sleep(1)

    def _exclamation(
        self, matrix: list[list[int]], start_row: int, start_col: int
    ) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._on
        matrix[start_col][start_row + 2] = self._on
        matrix[start_col][start_row + 3] = self._on
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col][start_row + 5] = self._on
        matrix[start_col][start_row + 6] = self._on
        matrix[start_col][start_row + 7] = self._on
        matrix[start_col][start_row + 8] = self._on
        matrix[start_col][start_row + 9] = self._on
        matrix[start_col][start_row + 10] = self._on
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._on
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._on
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 1][start_row + 5] = self._on
        matrix[start_col + 1][start_row + 6] = self._on
        matrix[start_col + 1][start_row + 7] = self._on
        matrix[start_col + 1][start_row + 8] = self._on
        matrix[start_col + 1][start_row + 9] = self._on
        matrix[start_col + 1][start_row + 10] = self._on
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._on
        matrix[start_col + 2][start_row + 3] = self._on
        matrix[start_col + 2][start_row + 4] = self._on
        matrix[start_col + 2][start_row + 5] = self._on
        matrix[start_col + 2][start_row + 6] = self._on
        matrix[start_col + 2][start_row + 7] = self._on
        matrix[start_col + 2][start_row + 8] = self._on
        matrix[start_col + 2][start_row + 9] = self._on
        matrix[start_col + 2][start_row + 10] = self._on
        matrix[start_col + 3][start_row] = self._on
        matrix[start_col + 3][start_row + 1] = self._on
        matrix[start_col + 3][start_row + 2] = self._on
        matrix[start_col + 3][start_row + 3] = self._on
        matrix[start_col + 3][start_row + 4] = self._on
        matrix[start_col + 3][start_row + 5] = self._on
        matrix[start_col + 3][start_row + 6] = self._on
        matrix[start_col + 3][start_row + 7] = self._on
        matrix[start_col + 3][start_row + 8] = self._on
        matrix[start_col + 3][start_row + 9] = self._on
        matrix[start_col + 3][start_row + 10] = self._on
