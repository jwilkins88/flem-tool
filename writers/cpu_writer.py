from time import sleep

import psutil

from writers.matrix_writer import MatrixWriter


class CpuWriter(MatrixWriter):
    __start_cords: tuple[int, int] = None
    __end_cords: tuple[int, int] = None
    running = True

    def __init__(
        self,
        on_bytes: int,
        off_bytes: int,
        start_coords: tuple[int, int],
        end_coords: tuple[int, int],
    ):
        super().__init__(on_bytes, off_bytes)
        self.writer_name = "CPU Writer"
        self.__start_cords = start_coords
        self.__end_cords = end_coords

    def write(self, matrix: list[list[int]], callback: callable) -> None:
        while self.running:
            for i in range(self.__start_cords[0], self.__end_cords[0]):
                for j in range(self.__start_cords[1], self.__end_cords[1]):
                    matrix[i][j] = self._off
            cpu_percentage = str(round(psutil.cpu_percent()))

            top_row = self.__start_cords[1]
            start_row = self.__start_cords[0]

            cpu_cols = len(cpu_percentage)

            if cpu_cols == 1:
                start_row = self.__end_cords[1] - 4
                # top_row = 29
            elif cpu_cols == 2:
                start_row = self.__end_cords[1] - 10
                # top_row = 23
            else:
                start_row = self.__end_cords[1] - 16
                # top_row = 17

            for char in cpu_percentage:
                self._write_number(char, matrix, start_row, self.__start_cords[0])
                start_row += 6

            callback()
            sleep(0.5)

    def stop(self):
        if self.running:
            self.running = False
