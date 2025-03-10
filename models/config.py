class ModulePositionConfig:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class ModuleConfig:
    def __init__(
        self,
        module_type: str,
        position: ModulePositionConfig,
        refresh_interval: int,
        arguments: dict = None,
    ):
        self.module_type = module_type
        self.position = position
        self.refresh_interval = refresh_interval
        self.arguments = arguments or {}


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
    ):
        self.name = name
        self.location = device_address
        self.speed = speed
        self.brightness = brightness
        self.on_bytes = on_bytes
        self.off_bytes = off_bytes
        self.modules = modules


class Config:
    def __init__(self, devices: list[DeviceConfig]):
        self.devices = devices
