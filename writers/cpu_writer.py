from time import sleep

from writers.matrix_writer import MatrixWriter


class CpuWriter(MatrixWriter):
    running = True

    def __init__(self, on_bytes, off_bytes):
        super().__init__(on_bytes, off_bytes)
        self.writer_name = "CPU Writer"

    def write(self, matrix: list[list[int]], callback: callable) -> None:
        column = 0
        row = 0
        max_row = 33
        max_column = 8
        while self.running:
            if row != 0:
                matrix[column][row - 1] = self._off
            elif column > 0 and row == 0:
                matrix[column - 1][max_row] = self._off
            elif column == 0 and row == 0:
                matrix[max_column][max_row] = self._off

            matrix[column][row] = self._on

            if row == max_row and column < max_column:
                row = 0
                column += 1
            elif column == max_column and row == max_row:
                row = 0
                column = 0
            else:
                row += 1
            callback()
            sleep(0.5)

    def stop(self):
        if self.running:
            self.running = False
