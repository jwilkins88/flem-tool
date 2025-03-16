# pylint: disable=abstract-method, missing-module-docstring
from typing import Callable

from loguru import logger

from flem.models.config_schema import ModuleSchema
from flem.models.modules.line_config import LineConfig, LineConfigSchema
from flem.modules.matrix_module import MatrixModule


class LineModule(MatrixModule):
    __config: LineConfig = None
    __width: int = None

    is_static = True
    module_name = "Line Module"

    def __init__(self, config: LineConfig, width: int = None, height: int = 1):
        super().__init__(config, width, height)

        if not isinstance(config, LineConfig):
            self.__config = LineConfigSchema().load(ModuleSchema().dump(config))
        else:
            self.__config = config

    def stop(self) -> None:
        self.running = False
        return super().stop()

    def write(
        self,
        update_device: Callable[[], None],
        write_queue: Callable[[tuple[int, int, bool]], None],
        execute_callback: bool = True,
        refresh_override: int = None,
    ) -> None:
        try:
            i = self.__config.position.x
            while i < self.__config.position.x + (
                self.__width or self.__config.arguments.width
            ):
                write_queue((i, self.__config.position.y, True))

                if self.__config.arguments.line_style == "dashed" and i % 2 != 0:
                    write_queue((i, self.__config.position.y, False))
                i += 1

                super().write(
                    update_device, write_queue, execute_callback, refresh_override
                )
        except (IndexError, ValueError, TypeError) as e:
            logger.exception(f"Error while running {self.module_name}: {e}")
            super().stop()
            super().clear_module(update_device, write_queue)
