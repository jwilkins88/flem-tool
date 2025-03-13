# pylint: disable=missing-module-docstring, missing-class-docstring, too-few-public-methods, too-many-positional-arguments, too-many-instance-attributes, too-many-arguments


class ModulePositionConfig:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class ModuleConfig:
    def __init__(
        self,
        name: str,
        module_type: str,
        position: ModulePositionConfig,
        refresh_interval: int,
        arguments: dict = None,
    ):
        self.name = name
        self.module_type = module_type
        self.position = position
        self.refresh_interval = refresh_interval
        self.arguments = arguments or {}


class SceneConfig:
    def __init__(
        self,
        name: str,
        show_for: int,
        scene_order: int,
        modules: list[str],
    ):
        self.name = name
        self.show_for = show_for
        self.scene_order = scene_order
        self.modules = modules


class DeviceConfig:
    def __init__(
        self,
        name: str,
        device_address: str,
        speed: int,
        brightness: int,
        on_bytes: int,
        off_bytes: int,
        modules: list[ModuleConfig],
        scenes: list[SceneConfig],
    ):
        self.name = name
        self.location = device_address
        self.speed = speed
        self.brightness = brightness
        self.on_bytes = on_bytes
        self.off_bytes = off_bytes
        self.modules = modules
        self.scenes = scenes


class Config:
    def __init__(
        self,
        devices: list[DeviceConfig],
    ):
        self.devices = devices
