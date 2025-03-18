# pylint: disable=abstract-method, missing-module-docstring
from typing import Callable

from loguru import logger

from flem.models.config_schema import ModuleSchema
from flem.models.modules.animator_config import (
    AnimatorConfig,
    AnimatorConfigSchema,
    AnimatorFrameSchema,
)
from flem.modules.matrix_module import MatrixModule


class AnimatorModule(MatrixModule):
    __config: AnimatorConfig = None
    from_frame = 0
    reset_frame = 0
    reset_delay = 0
    module_name = "Animator Module"

    def __init__(self, config: AnimatorConfig, width: int = 6, height: int = 4):
        super().__init__(config, width, height)

        if not isinstance(config, AnimatorConfig):
            self.__config = AnimatorConfigSchema().load(ModuleSchema().dump(config))
        else:
            self.__config = config

        if self.__config.arguments.animation_file:
            try:
                with open(
                    self.__config.arguments.animation_file, "r", encoding="utf-8"
                ) as file:
                    self.__config.arguments.frames = AnimatorFrameSchema().loads(
                        file.read(), many=True
                    )
            except (FileNotFoundError, SyntaxError, ValueError) as e:
                logger.exception(f"Failed to load animation frames: {e}")
                self.__config.arguments.frames = []

    def stop(self) -> None:
        self.running = False
        return super().stop()

    def start(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
    ):
        self.running = True
        self.reset()
        self.write(update_device, write_queue, execute_callback)

    def write(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
        refresh_override: int = None,
        running: bool = True,
    ) -> None:
        try:
            current_frame = 0
            while self.running:
                for row in range(self.__config.arguments.height):
                    for col in range(self.__config.arguments.width):
                        write_queue(
                            (
                                self.__config.position.x + col,
                                self.__config.position.y + row,
                                False,
                            )
                        )

                while current_frame < self.from_frame:
                    current_frame += 1

                if current_frame > len(self.__config.arguments.frames) - 1:
                    current_frame = self.reset_frame

                self._write_array(
                    self.__config.arguments.frames[current_frame].frame,
                    self.__config.position.x,
                    self.__config.position.y,
                    write_queue,
                )

                delay = self.__config.arguments.frames[current_frame].frame_duration

                if self.reset_delay != 0 and current_frame == self.reset_frame:
                    delay = self.reset_delay

                super().write(
                    update_device,
                    write_queue,
                    execute_callback,
                    delay,
                    self.running,
                )
                current_frame += 1
        except (IndexError, ValueError, TypeError) as e:
            logger.exception(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)
