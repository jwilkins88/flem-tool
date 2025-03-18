# pylint: disable=missing-module-docstring, missing-class-docstring, unused-argument

from marshmallow import Schema, fields, post_load

from flem.models.config import ModuleConfig, ModulePositionConfig
from flem.models.config_schema import ModulePositionSchema, ModuleSchema


class BatteryConfigArguments:
    def __init__(self, show_percentage: bool = False, critical_threshold: int = 20):
        self.show_percentage = show_percentage
        self.critical_threshold = critical_threshold


class BatteryConfig(ModuleConfig):
    def __init__(
        self,
        name: str,
        module_type: str,
        position: ModulePositionConfig,
        refresh_interval: int,
        arguments: BatteryConfigArguments,
    ):
        super().__init__(name, module_type, position, refresh_interval, arguments)
        self.arguments = arguments


class BatteryConfigArgumentsSchema(Schema):
    show_percentage = fields.Bool(required=False, load_default=False)
    critical_threshold = fields.Int(required=False, load_default=20)

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return BatteryConfigArguments(**data)


class BatteryConfigSchema(ModuleSchema):
    name = fields.Str()
    module_type = fields.Str()
    position = fields.Nested(ModulePositionSchema)
    refresh_interval = fields.Int()
    arguments = fields.Nested(BatteryConfigArgumentsSchema)

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return BatteryConfig(**data)
