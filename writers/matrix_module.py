# pylint: disable=missing-module-docstring

import abc


class MatrixModule:
    """
    MatrixModule is an abstract base class for writing matrix data. \
        It provides methods to write numbers and text into a matrix,
    as well as abstract methods that must be implemented by subclasses \
        to define specific behaviors for writing and blinking.

    Attributes:
        is_static (bool): Indicates if the module is static.
        writer_name (str): The name of the writer.
        running (bool): Indicates if the module is running.
        _on (int): The byte value representing the "on" state.
        _off (int): The byte value representing the "off" state.

    Methods:
        __init__(on_bytes: int, off_bytes: int):
            Initializes the MatrixModule with specified on and off byte values.

        write(matrix: list[list[int]], callback: callable, execute_callback: bool = True) -> None:
            Abstract method. Writes the matrix data and optionally executes a callback.

        stop() -> None:
            Abstract method. Stops the module.

        _write_number(number: str, matrix: list[list[int]], start_row: int, start_col: int) -> None:

        _write_text(text: str, matrix: list[list[int]], start_row: int, start_col: int) -> None:

        _blink(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Blinks the given text to the specified position in the matrix.

        _zero(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '0' into the matrix.

        _one(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '1' into the matrix.

        _two(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '2' into the matrix.

        _three(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '3' into the matrix.

        _four(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '4' into the matrix.

        _five(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '5' into the matrix.

        _six(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '6' into the matrix.

        _seven(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '7' into the matrix.

        _eight(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '8' into the matrix.

        _nine(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '9' into the matrix.

        _percent(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the '%' symbol into the matrix.

        _c(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the 'c' character into the matrix.

        _g(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the 'g' character into the matrix.

        _exclamation(matrix: list[list[int]], start_row: int, start_col: int) -> None:
            Abstract method. Writes the '!' character into the matrix.
    """

    __metaclass__ = abc.ABCMeta
    __number_funcs = {}
    __string_funcs = {}
    _on = None
    _off = None

    is_static = False
    writer_name = "Base Module"
    running = True

    def __init__(self, on_bytes: int, off_bytes: int):
        if on_bytes is None or off_bytes is None:
            raise ValueError("On and off bytes must be specified")

        self._off = off_bytes
        self._on = on_bytes

        self.__number_funcs = {
            "0": self._zero,
            "1": self._one,
            "2": self._two,
            "3": self._three,
            "4": self._four,
            "5": self._five,
            "6": self._six,
            "7": self._seven,
            "8": self._eight,
            "9": self._nine,
        }

        self.__string_funcs = {
            "%": self._percent,
            "g": self._g,
            "c": self._c,
            "!": self._exclamation,
        }

    @abc.abstractmethod
    def write(
        self, matrix: list[list[int]], callback: callable, execute_callback: bool = True
    ) -> None:
        "The main function that draws the matrix info for the module"
        if execute_callback:
            callback()

    @abc.abstractmethod
    def stop(self) -> None:
        """
        Stops the matrix module by setting the running flag to False.

        This method is used to signal the matrix module to stop its operations.
        """
        self.running = False

    def _write_number(
        self, number: str, matrix: list[list[int]], start_row: int, start_col: int
    ) -> None:
        """
        Writes a number into the given matrix starting at the specified row and column.

        Args:
            number (str): The number to write into the matrix.
            matrix (list of list of int): The matrix where the number will be written.
            start_row (int): The starting row index in the matrix.
            start_col (int): The starting column index in the matrix.

        Returns:
            bool: True if the number was successfully written, False otherwise.
        """
        self.__number_funcs[number](matrix, start_row, start_col)

    def _write_text(
        self, text: str, matrix: list[list[int]], start_row: int, start_col: int
    ) -> None:
        """
        Writes the given text to the specified position in the matrix.

        Args:
            text (str): The text to write into the matrix.
            matrix (list of list of any): The matrix where the text will be written.
            start_row (int): The starting row index in the matrix.
            start_col (int): The starting column index in the matrix.
        """
        self.__string_funcs[text](matrix, start_row, start_col)

    @abc.abstractmethod
    def _blink(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        """
        Blinks the given text to the specified position in the matrix.

        Args:
            text (str): The text to write into the matrix.
            matrix (list of list of any): The matrix where the text will be written.
            start_row (int): The starting row index in the matrix.
            start_col (int): The starting column index in the matrix.
        """

    @abc.abstractmethod
    def _zero(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._on
        matrix[start_col][start_row + 2] = self._on
        matrix[start_col][start_row + 3] = self._on
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._off
        matrix[start_col + 1][start_row + 2] = self._off
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._on
        matrix[start_col + 2][start_row + 3] = self._on
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _one(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._off
        matrix[start_col][start_row + 1] = self._on
        matrix[start_col][start_row + 2] = self._off
        matrix[start_col][start_row + 3] = self._off
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._on
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._on
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row] = self._off
        matrix[start_col + 2][start_row + 1] = self._off
        matrix[start_col + 2][start_row + 2] = self._off
        matrix[start_col + 2][start_row + 3] = self._off
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _two(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._off
        matrix[start_col][start_row + 2] = self._off
        matrix[start_col][start_row + 3] = self._on
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._off
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._off
        matrix[start_col + 2][start_row + 3] = self._off
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _three(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._off
        matrix[start_col][start_row + 2] = self._on
        matrix[start_col][start_row + 3] = self._off
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._off
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._on
        matrix[start_col + 2][start_row + 3] = self._on
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _four(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._on
        matrix[start_col][start_row + 2] = self._on
        matrix[start_col][start_row + 3] = self._off
        matrix[start_col][start_row + 4] = self._off
        matrix[start_col + 1][start_row] = self._off
        matrix[start_col + 1][start_row + 1] = self._off
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._off
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._on
        matrix[start_col + 2][start_row + 3] = self._on
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _five(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._on
        matrix[start_col][start_row + 2] = self._on
        matrix[start_col][start_row + 3] = self._off
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._off
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._off
        matrix[start_col + 2][start_row + 2] = self._off
        matrix[start_col + 2][start_row + 3] = self._on
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _six(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._on
        matrix[start_col][start_row + 2] = self._on
        matrix[start_col][start_row + 3] = self._on
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._off
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._off
        matrix[start_col + 2][start_row + 2] = self._on
        matrix[start_col + 2][start_row + 3] = self._on
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _seven(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._off
        matrix[start_col][start_row + 2] = self._off
        matrix[start_col][start_row + 3] = self._off
        matrix[start_col][start_row + 4] = self._off
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._off
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._on
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._off
        matrix[start_col + 2][start_row + 3] = self._off
        matrix[start_col + 2][start_row + 4] = self._off

    @abc.abstractmethod
    def _eight(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._on
        matrix[start_col][start_row + 2] = self._on
        matrix[start_col][start_row + 3] = self._on
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._off
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._on
        matrix[start_col + 2][start_row + 3] = self._on
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _nine(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._on
        matrix[start_col][start_row + 2] = self._on
        matrix[start_col][start_row + 3] = self._off
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._off
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._on
        matrix[start_col + 2][start_row + 3] = self._on
        matrix[start_col + 2][start_row + 4] = self._on

    # This is garbage
    # Don't Use this shit
    @abc.abstractmethod
    def _percent(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row] = self._on
        matrix[start_col][start_row + 1] = self._off
        matrix[start_col][start_row + 2] = self._off
        matrix[start_col][start_row + 3] = self._on
        matrix[start_col][start_row + 4] = self._off
        matrix[start_col + 1][start_row] = self._off
        matrix[start_col + 1][start_row + 1] = self._off
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._off
        matrix[start_col + 2][start_row] = self._off
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._off
        matrix[start_col + 2][start_row + 3] = self._off
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _c(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row + 1] = self._on
        matrix[start_col][start_row + 2] = self._on
        matrix[start_col][start_row + 3] = self._on
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col + 1][start_row + 1] = self._on
        matrix[start_col + 1][start_row + 2] = self._off
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._off
        matrix[start_col + 2][start_row + 3] = self._off
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _g(self, matrix: list[list[int]], start_row: int, start_col: int) -> None:
        matrix[start_col][start_row + 1] = self._on
        matrix[start_col][start_row + 2] = self._on
        matrix[start_col][start_row + 3] = self._on
        matrix[start_col][start_row + 4] = self._on
        matrix[start_col + 1][start_row + 1] = self._on
        matrix[start_col + 1][start_row + 2] = self._off
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._off
        matrix[start_col + 2][start_row + 3] = self._on
        matrix[start_col + 2][start_row + 4] = self._on

    @abc.abstractmethod
    def _exclamation(
        self, matrix: list[list[int]], start_row: int, start_col: int
    ) -> None:
        matrix[start_col][start_row] = self._off
        matrix[start_col][start_row + 1] = self._off
        matrix[start_col][start_row + 2] = self._off
        matrix[start_col][start_row + 3] = self._off
        matrix[start_col][start_row + 4] = self._off
        matrix[start_col + 1][start_row] = self._on
        matrix[start_col + 1][start_row + 1] = self._on
        matrix[start_col + 1][start_row + 2] = self._on
        matrix[start_col + 1][start_row + 3] = self._off
        matrix[start_col + 1][start_row + 4] = self._on
        matrix[start_col + 2][start_row] = self._on
        matrix[start_col + 2][start_row + 1] = self._on
        matrix[start_col + 2][start_row + 2] = self._on
        matrix[start_col + 2][start_row + 3] = self._off
        matrix[start_col + 2][start_row + 4] = self._on
