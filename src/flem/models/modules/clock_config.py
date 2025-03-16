# pylint: disable=missing-module-docstring, missing-class-docstring, unused-argument

from loguru import logger
from marshmallow import Schema, fields, post_load

from flem.models.config import ModuleConfig, ModulePositionConfig
from flem.models.config_schema import ModulePositionSchema, ModuleSchema


class ClockConfigArguments:
    def __init__(self, clock_mode: str, show_seconds_indicator: bool = False):
        self.clock_mode = clock_mode
        self.show_seconds_indicator = show_seconds_indicator


class ClockConfig(ModuleConfig):
    __clock_mode_options = ["12h", "24h"]

    def __init__(
        self,
        name: str,
        module_type: str,
        position: ModulePositionConfig,
        refresh_interval: int,
        arguments: ClockConfigArguments,
    ):
        if arguments.clock_mode not in self.__clock_mode_options:
            logger.warning("Invalid clock mode, defaulting to 12h")
            arguments.temperature_unit = "12h"

        super().__init__(name, module_type, position, refresh_interval, arguments)
        self.arguments = arguments


class ClockConfigArgumentsSchema(Schema):
    clock_mode = fields.Str()
    show_seconds_indicator = fields.Bool(required=False, missing=False)

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return ClockConfigArguments(**data)


class ClockConfigSchema(ModuleSchema):
    name = fields.Str()
    module_type = fields.Str()
    position = fields.Nested(ModulePositionSchema)
    refresh_interval = fields.Int()
    arguments = fields.Nested(ClockConfigArgumentsSchema)

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return ClockConfig(**data)
