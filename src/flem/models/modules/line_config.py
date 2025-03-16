# pylint: disable=missing-module-docstring, missing-class-docstring, unused-argument

from loguru import logger
from marshmallow import Schema, fields, post_load

from flem.models.config import ModuleConfig, ModulePositionConfig
from flem.models.config_schema import ModulePositionSchema, ModuleSchema


class LineConfigArguments:
    def __init__(self, line_style: str, width: int):
        self.line_style = line_style
        self.width = width


class LineConfig(ModuleConfig):
    __line_style_options = ["dashed", "solid"]

    def __init__(
        self,
        name: str,
        module_type: str,
        position: ModulePositionConfig,
        refresh_interval: int,
        arguments: LineConfigArguments,
    ):
        if arguments.line_style not in self.__line_style_options:
            logger.warning("Invalid line style, defaulting to solid")
            arguments.temperature_unit = "solid"

        super().__init__(name, module_type, position, refresh_interval, arguments)
        self.arguments = arguments


class LineConfigArgumentsSchema(Schema):
    line_style = fields.Str()
    width = fields.Int()

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return LineConfigArguments(**data)


class LineConfigSchema(ModuleSchema):
    name = fields.Str()
    module_type = fields.Str()
    position = fields.Nested(ModulePositionSchema)
    refresh_interval = fields.Int()
    arguments = fields.Nested(LineConfigArgumentsSchema)

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return LineConfig(**data)
