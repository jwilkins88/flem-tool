import abc


class MatrixWriter:
    __metaclass__ = abc.ABCMeta

    __number_funcs = {}
    __string_funcs = {}
    _on = None
    _off = None

    writer_name = "Base Writer"

    def __init__(self, on_bytes, off_bytes):
        if on_bytes is None or off_bytes is None:
            raise ValueError("On and off bytes must be specified")

        self._off = off_bytes
        self._on = on_bytes

        self.__number_funcs = {
            "0": self.__zero,
            "1": self.__one,
            "2": self.__two,
            "3": self.__three,
            "4": self.__four,
            "5": self.__five,
            "6": self.__six,
            "7": self.__seven,
            "8": self.__eight,
            "9": self.__nine,
        }
        self.__string_funcs = {"%": self.__percent, "g": self.__g, "c": self.__c}

    @abc.abstractmethod
    def write(self, matrix: list[list[int]], callback: callable) -> None:
        "The main function that draws the matrix info for the module"
        return

    @abc.abstractmethod
    def stop(self) -> None:
        return

    def _write_number(self, number, matrix, start_row, start_col):
        """
        Writes a number into the given matrix starting at the specified row and column.

        Args:
            number (int): The number to write into the matrix.
            matrix (list of list of int): The matrix where the number will be written.
            start_row (int): The starting row index in the matrix.
            start_col (int): The starting column index in the matrix.

        Returns:
            bool: True if the number was successfully written, False otherwise.
        """
        return self.__number_funcs[number](matrix, start_row, start_col)

    def _write_text(self, text, matrix, start_row, start_col):
        """
        Writes the given text to the specified position in the matrix.

        Args:
            text (str): The text to write into the matrix.
            matrix (list of list of any): The matrix where the text will be written.
            start_row (int): The starting row index in the matrix.
            start_col (int): The starting column index in the matrix.

        Returns:
            any: The result of the text writing operation, as defined by
                the specific string function.
        """
        return self.__string_funcs[text](matrix, start_row, start_col)

    def _print_divider(self, matrix, start_row, start_col, width, height):
        """
        Draws a divider on the given matrix starting from the specified position.

        Args:
            matrix (list of list of int): The matrix to draw the divider on.
            start_row (int): The starting row index (1-based).
            start_col (int): The starting column index (1-based).
            width (int): The width of the horizontal part of the divider.
            height (int): The height of the vertical part of the divider.

        Returns:
            list of list of int: The matrix with the divider drawn on it.
        """
        start_row = start_row - 1
        start_col = start_col - 1

        i = 0
        while i < width:
            matrix[start_col + i][start_row] = self._on
            i += 1

        max_col = start_col + i

        j = 0
        while j < height:
            matrix[max_col][start_row + j] = self._on

        return matrix

    def __zero(self, matrix, start_row, start_col):
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

        return matrix

    def __one(self, matrix, start_row, start_col):
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

        return matrix

    def __two(self, matrix, start_row, start_col):
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

        return matrix

    def __three(self, matrix, start_row, start_col):
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

        return matrix

    def __four(self, matrix, start_row, start_col):
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

        return matrix

    def __five(self, matrix, start_row, start_col):
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

        return matrix

    def __six(self, matrix, start_row, start_col):
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

        return matrix

    def __seven(self, matrix, start_row, start_col):
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

        return matrix

    def __eight(self, matrix, start_row, start_col):
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

        return matrix

    def __nine(self, matrix, start_row, start_col):
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

        return matrix

    # This is garbage
    # Don't Use this shit
    def __percent(self, matrix, start_row, start_col):
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

        return matrix

    def __c(self, matrix, start_row, start_col):
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

        return matrix

    def __g(self, matrix, start_row, start_col):
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

        return matrix
