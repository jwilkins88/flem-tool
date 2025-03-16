# pylint: disable=missing-module-docstring, missing-class-docstring, unused-argument

from marshmallow import Schema, fields, post_load

from flem.models.config import ModuleConfig, ModulePositionConfig
from flem.models.config_schema import ModulePositionSchema, ModuleSchema


class AnimatorFrame:
    def __init__(self, frame: list[list[int]], frame_duration: int):
        self.frame = frame
        self.frame_duration = frame_duration


class AnimatorConfigArguments:
    def __init__(
        self,
        frames: list[AnimatorFrame],
        width: int,
        height: int,
        animation_file: str = None,
    ):
        self.animation_file = animation_file
        self.frames = frames
        self.width = width
        self.height = height


class AnimatorConfig(ModuleConfig):

    def __init__(
        self,
        name: str,
        module_type: str,
        position: ModulePositionConfig,
        refresh_interval: int,
        arguments: AnimatorConfigArguments,
    ):
        super().__init__(name, module_type, position, refresh_interval, arguments)
        self.arguments = arguments


class AnimatorFrameSchema(Schema):
    frame = fields.List(fields.List(fields.Int))
    frame_duration = fields.Int()

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return AnimatorFrame(**data)


class AnimatorConfigArgumentsSchema(Schema):
    frames = fields.List(fields.Nested(AnimatorFrameSchema))
    width = fields.Int()
    height = fields.Int()
    animation_file = fields.Str(required=False, missing=None)

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return AnimatorConfigArguments(**data)


class AnimatorConfigSchema(ModuleSchema):
    name = fields.Str()
    module_type = fields.Str()
    position = fields.Nested(ModulePositionSchema)
    refresh_interval = fields.Int()
    arguments = fields.Nested(AnimatorConfigArgumentsSchema)

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return AnimatorConfig(**data)
