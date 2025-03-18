# pylint: disable=abstract-method, missing-module-docstring, too-many-locals
from datetime import datetime
from typing import Callable

from loguru import logger

from flem.models.config_schema import ModuleSchema
from flem.models.modules.clock_config import ClockConfig, ClockConfigSchema
from flem.modules.matrix_module import MatrixModule
from flem.models.config import ModuleConfig


class ClockModule(MatrixModule):
    __time_format_12h = "%I%M"
    __time_format_24h = "%H%M"
    __config: ClockConfig = None

    module_name = "Clock Module"

    def __init__(self, config: ModuleConfig, width: int = 9, height: int = 11):
        super().__init__(config, width, height)

        if not isinstance(config, ClockConfig):
            self.__config = ClockConfigSchema().load(ModuleSchema().dump(config))
        else:
            self.__config = config

    def start(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
    ):
        self.running = True
        self.reset()
        self.write(update_device, write_queue, execute_callback)

    def stop(self) -> None:
        self.running = False
        return super().stop()

    def write(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
        refresh_override: int = None,
        running: bool = True,
    ) -> None:
        try:
            while self.running:
                logger.debug(f"Module {self.__config.name} restarting main loop")
                time = datetime.now().strftime(
                    self.__time_format_12h
                    if self.__config.arguments.clock_mode == "12h"
                    else self.__time_format_24h
                )

                start_col = 0
                start_row = self.__config.position.y

                for i, char in enumerate(time):
                    if i == 2:
                        start_row += 6
                        start_col = 2
                    elif i == 3:
                        start_col = 6
                    self._write_object(char, write_queue, start_row, start_col)
                    if i < 2:
                        start_col += 4

                if self.__config.arguments.show_seconds_indicator:
                    seconds = int(datetime.now().strftime("%S"))
                    pips_to_show = super()._calculate_pips_to_show(seconds, 60, 10)

                    if pips_to_show == 0:
                        write_queue((8, self.__config.position.y, False))
                        write_queue((8, self.__config.position.y + 1, False))
                        write_queue((8, self.__config.position.y + 2, False))
                        write_queue((8, self.__config.position.y + 3, False))
                        write_queue((8, self.__config.position.y + 4, False))
                        write_queue((0, self.__config.position.y + 6, False))
                        write_queue((0, self.__config.position.y + 7, False))
                        write_queue((0, self.__config.position.y + 8, False))
                        write_queue((0, self.__config.position.y + 9, False))
                        write_queue((0, self.__config.position.y + 11, False))

                    pip_col = 8
                    buffer = 0
                    for i in range(pips_to_show):
                        if i > 4:
                            pip_col = 0
                            buffer = 1

                        write_queue(
                            (
                                pip_col,
                                self.__config.position.y + i + buffer,
                                seconds % 2 == 0,
                            )
                        )

                super().write(
                    update_device,
                    write_queue,
                    execute_callback,
                    refresh_override,
                    self.running,
                )
        except (IndexError, ValueError, TypeError) as e:
            logger.exception(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)
