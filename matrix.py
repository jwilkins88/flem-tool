# pylint: disable=missing-module-docstring

import threading
from device import Device
from writers import MatrixModule


class Matrix:
    """
    The Matrix class manages a matrix of devices and modules.
    """

    __DEFAULT_MATRIX = [
        [Device.OFF for _ in range(Device.HEIGHT)] for _ in range(Device.WIDTH)
    ]
    __BORDER_CHAR = "⬛"
    __ON_CHAR = "⚪"
    __OFF_CHAR = "⚫"
    __thread_list = []

    running = True

    def __init__(
        self,
        matrix_device: Device,
        modules: list[MatrixModule] = None,
        matrix: list[list[int]] = None,
    ):
        if not matrix_device:
            raise ValueError("No device specified")

        self.__modules = modules
        self.__device = matrix_device
        if self.__modules is None:
            self.__modules = []

        self._matrix = [row[:] for row in self.__DEFAULT_MATRIX]

        if matrix is not None:
            if (
                len(matrix) != matrix_device.WIDTH
                and len(matrix[0]) == matrix_device.HEIGHT
            ):
                raise ValueError(
                    f"""
                    Invalid matrix dimensions. Must be {matrix_device.WIDTH}x{matrix_device.HEIGHT}.
                    """
                )
            self._matrix = matrix
        if not self.__device.is_open():
            self.__device.connect()

    def start_modules(self) -> None:
        """
        Starts the modules associated with the matrix.

        This method iterates over the list of modules and starts each one. If a module is static,
        it writes directly to the matrix and update device. If a module is not static, it starts
        a new thread to handle the writing process and appends the thread to the thread list.

        Returns:
            None
        """
        for module in self.__modules:
            if module.is_static:
                module.write(self._matrix, self.__update_device)
                continue
            thread = threading.Thread(
                target=module.write,
                name=module.writer_name,
                args=(
                    self._matrix,
                    self.__update_device,
                ),
            )
            thread.start()
            self.__thread_list.append(thread)

    def set_matrix(self, matrix: list[list[int]]) -> None:
        """
        Sets the matrix to the given 2D list of integers and updates the device.
        This isn't really supposed to be used unless you want manual control of the matrix
        Prefer using writers

        Args:
            matrix (list[list[int]]): A 2D list representing the matrix to be set.

        Returns:
            None
        """
        self._matrix = matrix
        self.__update_device()

    def reset_matrix(self) -> None:
        """
        Resets the matrix to its default state.

        This method sets the matrix to a copy of the default matrix \
            and updates the device accordingly.
        """
        self._matrix = [row[:] for row in self.__DEFAULT_MATRIX]
        self.__update_device()

    def stop(self) -> None:
        """
        Stops the matrix processing by performing the following actions:

        1. Sets the running flag to False if it is currently True.
        2. Stops all modules in the __modules list.
        3. Joins all threads in the __thread_list to ensure they have completed.
        4. Resets the matrix to its initial state.
        5. Closes the device associated with the matrix.
        """
        if self.running:
            self.running = False

        for module in self.__modules:
            module.stop()

        for thread in self.__thread_list:
            thread.join()

        self.reset_matrix()
        self.__device.close()

    def __update_device(self) -> None:
        self.__device.render_matrix(self._matrix)

    def __str__(self):
        matrix_str = [self.__BORDER_CHAR for _ in range(self.__device.WIDTH * 2 - 2)]
        matrix_str.append("\n")

        row_index = 0
        while row_index < self.__device.HEIGHT:
            matrix_str.append(f"{self.__BORDER_CHAR} ")
            for column_index in range(self.__device.WIDTH):
                if self._matrix[column_index][row_index] == self.__device.ON:
                    matrix_str.append(self.__ON_CHAR)
                    matrix_str.append(" ")
                else:
                    matrix_str.append(self.__OFF_CHAR)
                    matrix_str.append(" ")

            matrix_str.append(self.__BORDER_CHAR)
            matrix_str.append("\n")
            row_index += 1

        matrix_str.append(
            "".join([self.__BORDER_CHAR for _ in range(self.__device.WIDTH * 2 - 2)])
        )

        return "".join(map(str, matrix_str))
