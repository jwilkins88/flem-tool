from threading import Thread, Timer
from typing import Callable

from models import SceneConfig
from modules import MatrixModule


class Scene:
    __update_device: Callable[[], None]
    __write_queue: Callable[[tuple[int, int, bool]], None]
    __scene_finished: callable
    __config: SceneConfig
    __modules: list[MatrixModule]
    __threads: list[Thread]
    __timer: Timer
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
        self.running = True
        print(f"Running scene {self.__config.name}")

        for module in self.__modules:
            if module.is_static:
                module.start(self.__update_device, self.__write_queue)
                continue

            thread = Thread(
                target=module.start,
                name=f"{module.module_name}_{id(self)}",
                args=(
                    self.__update_device,
                    self.__write_queue,
                ),
                daemon=True,
            )
            self.__threads.append(thread)

            thread.start()

        if self.__config.show_for != 0:
            self.__timer = Timer(
                self.__config.show_for / 1000, self.__scene_finished, args=(self,)
            )
            self.__timer.start()

    def stop(self):
        self.running = False
        print(f"Stopping scene {self.__config.name}")

        try:
            self.__timer.join(2)
        except:
            pass

        for module in self.__modules:
            try:
                module.stop()
            except:
                pass

        for thread in self.__threads:
            try:
                thread.join(timeout=2)
            except:
                pass

        self.__threads.clear()
