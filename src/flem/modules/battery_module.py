# pylint: disable=abstract-method, missing-module-docstring, too-many-locals
import os
from typing import Callable
from threading import Thread

from loguru import logger
import psutil

from flem.models.config_schema import ModuleSchema
from flem.models.modules.animator_config import AnimatorConfig, AnimatorConfigArguments
from flem.models.modules.battery_config import BatteryConfig, BatteryConfigSchema
from flem.modules.animator_module import AnimatorModule
from flem.modules.matrix_module import MatrixModule
from flem.models.config import ModuleConfig, ModulePositionConfig


class BatteryModule(MatrixModule):
    __config: BatteryConfig = None
    __animator_files_root = f"{os.path.expanduser('~')}/.flem/animator_files"
    __charging_animation: AnimatorModule = None
    __charging_thread: Thread = None

    module_name = "Battery Module"

    def __init__(self, config: ModuleConfig, width: int = 9, height: int = 11):
        super().__init__(config, width, height)

        if not isinstance(config, BatteryConfig):
            self.__config = BatteryConfigSchema().load(ModuleSchema().dump(config))
        else:
            self.__config = config

        self.__charging_animation = AnimatorModule(
            AnimatorConfig(
                name="Battery Charging Animation",
                position=ModulePositionConfig(
                    self.__config.position.x + 1, self.__config.position.y + 1
                ),
                arguments=AnimatorConfigArguments(
                    frames=[],
                    animation_file=f"{self.__animator_files_root}/battery/charging.json",
                    width=7,
                    height=2,
                ),
                refresh_interval=0,
                module_type="AnimatorModule",
            )
        )
        self.__charging_animation.reset_delay = 2000
        self.__charging_animation.running = False

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
        if self.__charging_animation.running:
            self.__charging_animation.stop()

        if self.__charging_thread and self.__charging_thread.is_alive():
            self.__charging_thread.join(self.__config.refresh_interval)

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
            blink_status = False
            self._write_object(
                "battery",
                write_queue,
                self.__config.position.y,
                self.__config.position.x,
            )
            while self.running:
                logger.debug(f"Module {self.__config.name} restarting main loop")

                battery_info = psutil.sensors_battery()

                battery_pips = self._calculate_pips_to_show(
                    battery_info.percent, 100, 14
                )

                self.__charging_animation.from_frame = battery_pips
                self.__charging_animation.reset_frame = (
                    0 if battery_pips == 0 else battery_pips - 1
                )

                if battery_info.power_plugged and not self.__charging_animation.running:
                    self.__charging_thread = Thread(
                        target=self.__charging_animation.start,
                        args=(update_device, write_queue, True),
                    )
                    self.__charging_thread.start()
                elif (
                    not battery_info.power_plugged and self.__charging_animation.running
                ):
                    self.__charging_animation.stop()
                    if self.__charging_thread:
                        self.__charging_thread.join(self.__config.refresh_interval)

                if not battery_info.power_plugged:
                    is_battery_critical = (
                        battery_info.percent
                        <= self.__config.arguments.critical_threshold
                    )
                    start_row = self.__config.position.y + 1
                    start_col = self.__config.position.x + 1
                    should_blink = False
                    if is_battery_critical:
                        should_blink = True
                        blink_status = not blink_status
                    else:
                        should_blink = False

                    for i in range(14):
                        pip_on = i < battery_pips
                        if not should_blink and i == battery_pips - 1:
                            should_blink = True
                            blink_status = not blink_status

                        if i % 2 == 0:
                            write_queue(
                                (
                                    start_col,
                                    start_row,
                                    (
                                        blink_status
                                        if should_blink and pip_on
                                        else pip_on
                                    ),
                                )
                            )
                        else:
                            write_queue(
                                (
                                    start_col,
                                    start_row + 1,
                                    (
                                        blink_status
                                        if should_blink and pip_on
                                        else pip_on
                                    ),
                                )
                            )
                            start_col += 1

                if self.__config.arguments.show_percentage:
                    percentage = str(round(battery_info.percent))

                    if len(percentage) == 1:
                        percentage = "0" + percentage

                    start_col = self.__config.position.x + 1
                    for char in percentage:
                        self._write_object(
                            char,
                            write_queue,
                            self.__config.position.y + 5,
                            start_col,
                        )
                        start_col += 4

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
