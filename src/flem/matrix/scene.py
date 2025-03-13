from threading import Thread, Timer
from typing import Callable

from loguru import logger

from flem.models.config import SceneConfig
from flem.modules.matrix_module import MatrixModule


class Scene:
    __update_device: Callable[[], None]
    __write_queue: Callable[[tuple[int, int, bool]], None]
    __scene_finished: callable
    __config: SceneConfig
    __modules: list[MatrixModule]
    __threads: list[Thread]
    __timer: Timer = None
    running: bool = False

    def __init__(
        self,
        config: SceneConfig,
        modules: list[MatrixModule],
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        scene_finished: callable,
    ):
        self.__config = config
        self.__modules = modules
        self.__update_device = update_device
        self.__write_queue = write_queue
        self.__scene_finished = scene_finished
        self.__threads: list[Thread] = []

    def start(self):
        """
        Starts the scene by initializing and starting all modules and setting up a timer if
        required.
        This method performs the following steps:
        1. Sets the `running` attribute to True and prints the name of the scene.
        2. Iterates over all modules in `self.__modules`:
            - If a module is static, it starts the module directly.
            - If a module is not static, it starts the module in a new thread and track the thread.
        3. If `show_for` is not 0, sets up a timer to call stop the scene after the specified
        duration
        """

        self.running = True
        logger.info(f"Running scene {self.__config.name}")

        for module in self.__modules:
            logger.info(f"Starting module {module.module_name}")
            if module.is_static:
                logger.debug(f"{module.module_name} is static")
                module.start(self.__update_device, self.__write_queue)
                continue

            logger.debug(f"{module.module_name} is threaded")
            thread = Thread(
                target=module.start,
                name=f"{module.module_name}_{id(self)}",
                args=(
                    self.__update_device,
                    self.__write_queue,
                ),
            )
            logger.debug(f"Started thread {thread.name} for {module.module_name}")
            self.__threads.append(thread)

            thread.start()

        if self.__config.show_for != 0:
            logger.debug(
                f"Setting up timer for {self.__config.show_for}ms for scene {self.__config.name}"
            )
            self.__timer = Timer(
                self.__config.show_for / 1000, self.__scene_finished, args=(self,)
            )
            self.__timer.start()

    def stop(self):
        """
        Stops the scene by performing the following actions:
        1. Attempts to join the timer thread with a timeout of 2 seconds.
        2. Iterates through all modules and attempts to stop each one.
        3. Iterates through all threads and attempts to join each one with a timeout of 2 seconds.
        4. Clears the list of threads.
        Exceptions during stopping of modules and threads are caught and ignored.
        """
        logger.info(f"Stopping scene {self.__config.name}")
        self.running = False

        for module in self.__modules:
            try:
                logger.debug(f"Stopping module {module.module_name}")
                module.stop()
            except (RuntimeError, TimeoutError) as e:
                logger.error(
                    f"Error while stopping {module.module_name} in scene {self.__config.name}: {e}"
                )

        try:
            if self.__timer and not self.__timer.is_alive():
                logger.debug(f"Attempting to join timer for scene {self.__config.name}")
                self.__timer.join()
        except (RuntimeError, TimeoutError) as e:
            logger.error(
                f"Error while joining timer for scene {self.__config.name}: {e}"
            )

        for thread in self.__threads:
            try:
                logger.debug(f"Attempting to join thread {thread.name}")
                if thread.is_alive():
                    thread.join()
            except (RuntimeError, TimeoutError) as e:
                logger.error(f"Error while joining thread {thread.name}: {e}")

        self.__threads.clear()
