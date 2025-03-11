# pylint: disable=missing-module-docstring

from threading import Thread, Lock
import queue

from led_device import LedDevice
from models import SceneConfig
from modules import MatrixModule
from scene import Scene


class Matrix:
    """
    The Matrix class manages a matrix of devices and modules.
    """

    __DEFAULT_MATRIX: list[list[int]] = [
        [LedDevice.OFF for _ in range(LedDevice.HEIGHT)] for _ in range(LedDevice.WIDTH)
    ]
    __BORDER_CHAR: str = "⬛"
    __ON_CHAR: str = "⚪"
    __OFF_CHAR: str = "⚫"
    __thread_list: list[Thread] = None
    __change_queue: queue.Queue = None
    __lock: Lock = None
    __scenes: list[Scene]
    __current_scene: int = 0

    running: bool = True
    name = None

    def __init__(
        self,
        matrix_device: LedDevice,
        modules: list[MatrixModule] = None,
        matrix: list[list[int]] = None,
        scenes: list[SceneConfig] = None,
    ):
        if not matrix_device:
            raise ValueError("No device specified")

        self.__modules = modules
        self.__device = matrix_device
        if self.__modules is None:
            self.__modules = []

        self._matrix = [row[:] for row in self.__DEFAULT_MATRIX]
        self.__change_queue = queue.Queue()
        self.__lock = Lock()
        self.__scenes = []
        for scene in scenes:
            scene_modules = []
            for module in scene.modules:
                for module in self.__modules:
                    if module.module_name in scene.modules:
                        scene_modules.append(module)
                        continue
            self.__scenes.append(
                Scene(
                    scene,
                    scene_modules,
                    self.__update_device,
                    self.__write_queue,
                    self.__scene_finished,
                )
            )
        self.name = self.__device.name

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

    def run_next_scene(self) -> None:
        """
        Runs the scenes associated with the matrix.

        This method iterates over the list of scenes and runs each one. It writes the modules
        associated with the scene to the matrix and updates the device. The scene is then shown
        for the specified duration.

        Returns:
            None
        """
        self.__scenes[self.__current_scene].start()

        self.__current_scene = self.__current_scene + 1
        if self.__current_scene > len(self.__scenes) - 1:
            self.__current_scene = 0

    def reset_matrix(self, update_device: bool = True) -> None:
        """
        Resets the matrix to its default state.

        This method sets the matrix to a copy of the default matrix \
            and updates the device accordingly.
        """
        with self.__lock:
            self._matrix = [row[:] for row in self.__DEFAULT_MATRIX]

        if update_device:
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
        self.__change_queue.shutdown()
        if self.running:
            self.running = False

        for scene in self.__scenes:
            try:
                scene.stop()
            except:
                pass

        try:
            self.reset_matrix()
            self.__device.close()
        except:
            pass

    def __stop_scene(self, scene: Scene) -> None:
        """
        Stops the given scene by resetting the matrix to its default state.

        Args:
            scene (SceneConfig): The scene to be stopped.

        Returns:
            None
        """
        scene.stop()

        self.reset_matrix(False)

    def __scene_finished(self, scene: Scene):
        self.__stop_scene(scene)
        self.run_next_scene()

    def __write_queue(self, value: tuple[int, int, bool]) -> None:
        """
        Writes the given value to the matrix.

        Args:
            value (list[tuple[int, int, bool]]): A list of tuples containing the x and y coordinates
                of the matrix and a boolean value indicating whether the LED should be on or off.

        Returns:
            None
        """
        try:
            self.__change_queue.put(value, block=False)
        except queue.ShutDown:
            pass

    def __update_device(self) -> None:
        # print(self.__change_queue)
        while not self.__change_queue.empty() and not self.__change_queue.is_shutdown:
            try:
                with self.__lock:
                    x, y, on = self.__change_queue.get(block=False)
                    self._matrix[x][y] = self.__device.ON if on else self.__device.OFF
            except queue.Empty:
                break
            except IndexError:
                print(f"[{x}][{y}]")
                raise
        try:
            self.__device.render_matrix(self._matrix)
        except Exception as e:
            print("Error updating device: ", e)

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
