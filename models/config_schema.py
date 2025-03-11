from marshmallow import Schema, fields, post_load

from .config import (
    Config,
    DeviceConfig,
    ModuleConfig,
    ModulePositionConfig,
    SceneConfig,
)


class ModulePositionSchema(Schema):
    x = fields.Int()
    y = fields.Int()

    @post_load
    def make_module_position(self, data, **kwargs):
        return ModulePositionConfig(**data)


class ModuleSchema(Schema):
    name = fields.Str()
    module_type = fields.Str()
    position = fields.Nested(ModulePositionSchema)
    refresh_interval = fields.Int()
    arguments = fields.Dict(required=False)

    @post_load
    def make_module(self, data, **kwargs):
        return ModuleConfig(**data)


class SceneSchema(Schema):
    name = fields.Str()
    show_for = fields.Int()
    scene_order = fields.Int()
    modules = fields.List(fields.Str())

    @post_load
    def make_scene(self, data, **kwargs):
        return SceneConfig(**data)


class DeviceSchema(Schema):
    name = fields.Str()
    device_address = fields.Str()
    speed = fields.Int()
    brightness = fields.Int()
    on_bytes = fields.Int()
    off_bytes = fields.Int()
    modules = fields.List(fields.Nested(ModuleSchema))
    scenes = fields.List(fields.Nested(SceneSchema))

    @post_load
    def make_device(self, data, **kwargs):
        return DeviceConfig(**data)


class ConfigSchema(Schema):
    devices = fields.List(fields.Nested(DeviceSchema))

    @post_load
    def make_config(self, data, **kwargs):
        return Config(**data)
