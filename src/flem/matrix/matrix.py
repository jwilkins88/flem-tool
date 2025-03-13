# pylint: disable=missing-module-docstring

from threading import Lock
import queue

from loguru import logger

from flem.devices.led_device import LedDevice
from flem.models.config import SceneConfig
from flem.modules.matrix_module import MatrixModule
from flem.matrix.scene import Scene


class Matrix:
    """
    Matrix class for managing and controlling an LED matrix device.
    Attributes:
        running (bool): Flag indicating whether the matrix is running.
        name (str): Name of the matrix device.
    Methods:
        __init__(self, matrix_device: LedDevice, modules: list[MatrixModule] = None,
        matrix: list[list[int]] = None, scenes: list[SceneConfig] = None):
            Initializes the Matrix object with the given device, modules, matrix,
            and scenes.
        set_matrix(self, matrix: list[list[int]]) -> None:
        run_next_scene(self) -> None:
            Runs the next scene in the list of scenes.
        reset_matrix(self, update_device: bool = True) -> None:
        stop(self) -> None:
            Stops the matrix processing and resets the matrix to its initial state.
    """

    __DEFAULT_MATRIX: list[list[int]] = [
        [LedDevice.OFF for _ in range(LedDevice.HEIGHT)] for _ in range(LedDevice.WIDTH)
    ]
    __BORDER_CHAR: str = "⬛"
    __ON_CHAR: str = "⚪"
    __OFF_CHAR: str = "⚫"
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
        """
        Initialize the Matrix class.
        Args:
            matrix_device (LedDevice): The LED device to control the matrix.
            modules (list[MatrixModule], optional): A list of matrix modules. Defaults to None.
            matrix (list[list[int]], optional): A 2D list representing the matrix. Defaults to None.
            scenes (list[SceneConfig], optional): A list of scene configurations. Defaults to None.
        Raises:
            ValueError: If no device is specified or if the matrix dimensions are invalid.
        """
        if not matrix_device:
            logger.error("No device specified")
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
                        if any(
                            module.module_name in scene_module.module_name
                            for scene_module in scene_modules
                        ):
                            continue
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
                logger.error(
                    (
                        "Invalid matrix dimensions. Must be",
                        f" {matrix_device.WIDTH}x{matrix_device.HEIGHT}.",
                    )
                )
                raise ValueError(
                    (
                        "Invalid matrix dimensions. Must be ",
                        f" {matrix_device.WIDTH}x{matrix_device.HEIGHT}.",
                    )
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
        logger.debug("Running next scene")
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
        logger.debug("Resetting matrix")
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
        logger.debug(f"Stopping matrix {self.name}")
        logger.debug("Shutting down change queue")
        self.__change_queue.shutdown()
        if self.running:
            self.running = False

        for scene in self.__scenes:
            try:
                scene.stop()
            except Exception as e:
                logger.exception(f"Error while stopping scene: {e}")

        try:
            self.reset_matrix()
            logger.debug("Closing device")
            self.__device.close()
        except Exception as e:
            logger.exception(f"Error while stopping matrix: {e}")

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
        try:
            logger.debug(f"Writing value to queue: {value}")
            self.__change_queue.put(value, block=False)
        except queue.ShutDown:
            logger.debug("Queue is shutdown")

    def __update_device(self) -> None:
        logger.debug("Updating device")
        logger.debug("Reading changes from queue")
        with self.__lock:
            while (
                not self.__change_queue.empty() and not self.__change_queue.is_shutdown
            ):
                try:
                    x, y, on = self.__change_queue.get(block=False)
                    self._matrix[x][y] = on
                except queue.Empty as e:
                    logger.debug(f"Queue is empty: {e}")
                    break
                except IndexError as ie:
                    logger.exception(f"[{x}][{y}] Index out of bounds: {ie}")
                    raise
        try:
            logger.debug("Rendering matrix")
            self.__device.render_matrix(self._matrix)
        except Exception as e:
            logger.exception(f"Error updating device: {e}")

    def __str__(self):
        matrix_str = [self.__BORDER_CHAR for _ in range(self.__device.WIDTH * 2 - 2)]
        matrix_str.append("\n")

        row_index = 0
        while row_index < self.__device.HEIGHT:
            matrix_str.append(f"{self.__BORDER_CHAR} ")
            for column_index in range(self.__device.WIDTH):
                if self._matrix[column_index][row_index]:
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
