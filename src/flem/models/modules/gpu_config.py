# pylint: disable=missing-module-docstring, missing-class-docstring, unused-argument

from marshmallow import Schema, fields, post_load

from flem.models.config import ModuleConfig, ModulePositionConfig
from flem.models.config_schema import ModulePositionSchema, ModuleSchema


class GpuConfigArguments:
    def __init__(
        self,
        gpu_command: str,
        gpu_command_arguments: list[str],
        gpu_index: int = 0,
        gpu_temp_property: str = "temp",
        gpu_util_property: str = "gpu_util",
        show_temp: bool = False,
        use_bar_graph: bool = False,
    ):
        self.show_temp = show_temp
        self.use_bar_graph = use_bar_graph
        self.gpu_command = gpu_command
        self.gpu_index = gpu_index
        self.gpu_command_arguments = gpu_command_arguments
        self.gpu_temp_argument = gpu_temp_property
        self.gpu_util_argument = gpu_util_property


class GpuConfig(ModuleConfig):
    def __init__(
        self,
        name: str,
        module_type: str,
        position: ModulePositionConfig,
        refresh_interval: int,
        arguments: GpuConfigArguments,
    ):
        super().__init__(name, module_type, position, refresh_interval, arguments)
        self.arguments = arguments


class GpuConfigArgumentsSchema(Schema):
    gpu_command = fields.Str()
    gpu_command_arguments = fields.List(fields.Str())
    gpu_index = fields.Int()
    gpu_temp_property = fields.Str()
    gpu_util_property = fields.Str()
    show_temp = fields.Bool(required=False, missing=False)
    use_bar_graph = fields.Bool(required=False, missing=False)

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return GpuConfigArguments(**data)


class GpuConfigSchema(ModuleSchema):
    name = fields.Str()
    module_type = fields.Str()
    position = fields.Nested(ModulePositionSchema)
    refresh_interval = fields.Int()
    arguments = fields.Nested(GpuConfigArgumentsSchema)

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return GpuConfig(**data)
