# pylint: disable=missing-module-docstring

import abc
from typing import Callable

from loguru import logger

from flem.models.config import ModuleConfig


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

    Methods:
        __init__(on_bytes: int, off_bytes: int):
            Initializes the MatrixModule with specified on and off byte values.

        write(callback: callable, execute_callback: bool = True) -> None:
            Abstract method. Writes the matrix data and optionally executes a callback.

        stop() -> None:
            Abstract method. Stops the module.

        _write_number(number: str, start_row: int, start_col: int) -> None:

        _write_text(text: str, start_row: int, start_col: int) -> None:

        _blink(start_row: int, start_col: int) -> None:
            Abstract method. Blinks the given text to the specified position in the matrix.

        _zero(start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '0' into the matrix.

        _one(start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '1' into the matrix.

        _two(start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '2' into the matrix.

        _three(start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '3' into the matrix.

        _four(start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '4' into the matrix.

        _five(start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '5' into the matrix.

        _six(mstart_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '6' into the matrix.

        _seven(start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '7' into the matrix.

        _eight(start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '8' into the matrix.

        _nine(start_row: int, start_col: int) -> None:
            Abstract method. Writes the digit '9' into the matrix.

        _percent(start_row: int, start_col: int) -> None:
            Abstract method. Writes the '%' symbol into the matrix.

        _c(start_row: int, start_col: int) -> None:
            Abstract method. Writes the 'c' character into the matrix.

        _g(start_row: int, start_col: int) -> None:
            Abstract method. Writes the 'g' character into the matrix.

        _exclamation(start_row: int, start_col: int) -> None:
            Abstract method. Writes the '!' character into the matrix.
    """

    __metaclass__ = abc.ABCMeta
    __number_funcs = None
    __string_funcs = None
    __config: ModuleConfig = None
    __width: int = None
    __height: int = None

    is_static = False
    module_name: str = "Base Module"
    running = True

    def __init__(self, config: ModuleConfig, width: int, height: int):
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
            "!": self._exclamation,
            "b": self._b,
            "c": self._c,
            "g": self._g,
            "p": self._p,
            "u": self._u,
        }

        self.__config = config
        self.__width = width
        self.__height = height
        self.module_name = config.name

    @abc.abstractmethod
    def start(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
    ):
        self.running = True
        self.reset()
        self.write(update_device, write_queue, execute_callback)

    @abc.abstractmethod
    def reset(self) -> None:
        pass

    @abc.abstractmethod
    def stop(self) -> None:
        """
        Stops the matrix module by setting the running flag to False.

        This method is used to signal the matrix module to stop its operations.
        """
        self.running = False

    @abc.abstractmethod
    def write(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
    ) -> None:
        "The main function that draws the matrix info for the module"
        if execute_callback:
            try:
                update_device()
            except Exception as e:
                logger.exception(f"An error occurred while updating the device: {e}")

    @abc.abstractmethod
    def clear_module(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
    ) -> None:
        """
        Clears the matrix by setting all values to False.

        This method is used to clear the matrix of any data.
        """
        try:
            for row in range(
                self.__config.position.y, self.__config.position.y + self.__height
            ):
                for col in range(
                    self.__config.position.x, self.__config.position.x + self.__width
                ):
                    write_queue((col, row, False))

            update_device()
        except Exception as e:
            logger.exception(f"An error occurred while clearing the module: {e}")

    def _write_number(
        self,
        number: str,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
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
        self.__number_funcs[number](write_queue, start_row, start_col)

    def _write_text(
        self,
        text: str,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        """
        Writes the given text to the specified position in the matrix.

        Args:
            text (str): The text to write into the matrix.
            matrix (list of list of any): The matrix where the text will be written.
            start_row (int): The starting row index in the matrix.
            start_col (int): The starting column index in the matrix.
        """
        self.__string_funcs[text](write_queue, start_row, start_col)

    @abc.abstractmethod
    def _blink(self, start_row: int, start_col: int) -> None:
        """
        Blinks the given text to the specified position in the matrix.

        Args:
            text (str): The text to write into the matrix.
            matrix (list of list of any): The matrix where the text will be written.
            start_row (int): The starting row index in the matrix.
            start_col (int): The starting column index in the matrix.
        """

    @abc.abstractmethod
    def _calculate_pips_to_show(
        self, value: float, max_value: float, max_pips: int
    ) -> int:
        pip_value = max_pips / max_value

        return round(pip_value * value)

    @abc.abstractmethod
    def _zero(
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
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, False))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))
        write_queue((start_col + 2, start_row + 4, True))

    @abc.abstractmethod
    def _one(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, False))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, False))
        write_queue((start_col, start_row + 3, False))
        write_queue((start_col, start_row + 4, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, True))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, True))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 2, start_row, False))
        write_queue((start_col + 2, start_row + 1, False))
        write_queue((start_col + 2, start_row + 2, False))
        write_queue((start_col + 2, start_row + 3, False))
        write_queue((start_col + 2, start_row + 4, True))

    @abc.abstractmethod
    def _two(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, False))
        write_queue((start_col, start_row + 2, False))
        write_queue((start_col, start_row + 3, True))
        write_queue((start_col, start_row + 4, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, False))
        write_queue((start_col + 2, start_row + 3, False))
        write_queue((start_col + 2, start_row + 4, True))

    @abc.abstractmethod
    def _three(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, False))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, False))
        write_queue((start_col, start_row + 4, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))
        write_queue((start_col + 2, start_row + 4, True))

    @abc.abstractmethod
    def _four(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, False))
        write_queue((start_col, start_row + 4, False))
        write_queue((start_col + 1, start_row, False))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 1, start_row + 4, False))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))
        write_queue((start_col + 2, start_row + 4, True))

    @abc.abstractmethod
    def _five(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, False))
        write_queue((start_col, start_row + 4, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, False))
        write_queue((start_col + 2, start_row + 2, False))
        write_queue((start_col + 2, start_row + 3, True))
        write_queue((start_col + 2, start_row + 4, True))

    @abc.abstractmethod
    def _six(
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
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, False))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))
        write_queue((start_col + 2, start_row + 4, True))

    @abc.abstractmethod
    def _seven(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, False))
        write_queue((start_col, start_row + 2, False))
        write_queue((start_col, start_row + 3, False))
        write_queue((start_col, start_row + 4, False))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, True))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, False))
        write_queue((start_col + 2, start_row + 3, False))
        write_queue((start_col + 2, start_row + 4, False))

    @abc.abstractmethod
    def _eight(
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
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))
        write_queue((start_col + 2, start_row + 4, True))

    @abc.abstractmethod
    def _nine(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, False))
        write_queue((start_col, start_row + 4, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))
        write_queue((start_col + 2, start_row + 4, True))

    # This is garbage
    # Don't Use this
    @abc.abstractmethod
    def _percent(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, False))
        write_queue((start_col, start_row + 2, False))
        write_queue((start_col, start_row + 3, True))
        write_queue((start_col, start_row + 4, False))
        write_queue((start_col + 1, start_row, False))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 1, start_row + 4, False))
        write_queue((start_col + 2, start_row, False))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, False))
        write_queue((start_col + 2, start_row + 3, False))
        write_queue((start_col + 2, start_row + 4, True))

    @abc.abstractmethod
    def _b(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, True))
        write_queue((start_col + 1, start_row, False))
        write_queue((start_col + 1, start_row + 1, True))
        write_queue((start_col + 1, start_row + 2, False))
        write_queue((start_col + 1, start_row + 3, True))
        write_queue((start_col + 2, start_row, False))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))

    @abc.abstractmethod
    def _c(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, False))
        write_queue((start_col + 1, start_row + 3, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, False))
        write_queue((start_col + 2, start_row + 2, False))
        write_queue((start_col + 2, start_row + 3, True))

    @abc.abstractmethod
    def _g(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, False))
        write_queue((start_col + 1, start_row + 3, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, False))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))

    @abc.abstractmethod
    def _p(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, True))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, False))

    @abc.abstractmethod
    def _u(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, True))
        write_queue((start_col, start_row + 1, True))
        write_queue((start_col, start_row + 2, True))
        write_queue((start_col, start_row + 3, True))
        write_queue((start_col + 1, start_row, False))
        write_queue((start_col + 1, start_row + 1, False))
        write_queue((start_col + 1, start_row + 2, False))
        write_queue((start_col + 1, start_row + 3, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, True))

    @abc.abstractmethod
    def _exclamation(
        self,
        write_queue: Callable[[tuple[int, int, bool]], None],
        start_row: int,
        start_col: int,
    ) -> None:
        write_queue((start_col, start_row, False))
        write_queue((start_col, start_row + 1, False))
        write_queue((start_col, start_row + 2, False))
        write_queue((start_col, start_row + 3, False))
        write_queue((start_col, start_row + 4, False))
        write_queue((start_col + 1, start_row, True))
        write_queue((start_col + 1, start_row + 1, True))
        write_queue((start_col + 1, start_row + 2, True))
        write_queue((start_col + 1, start_row + 3, False))
        write_queue((start_col + 1, start_row + 4, True))
        write_queue((start_col + 2, start_row, True))
        write_queue((start_col + 2, start_row + 1, True))
        write_queue((start_col + 2, start_row + 2, True))
        write_queue((start_col + 2, start_row + 3, False))
        write_queue((start_col + 2, start_row + 4, True))
