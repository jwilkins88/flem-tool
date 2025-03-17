import pytest
from flem.models.config import (
    ModulePositionConfig,
    ModuleConfig,
    SceneConfig,
    DeviceConfig,
    Config,
)


def test_module_position_config():
    """Test initialization of ModulePositionConfig."""
    position = ModulePositionConfig(x=10, y=20)
    assert position.x == 10
    assert position.y == 20


def test_module_config():
    """Test initialization of ModuleConfig."""
    position = ModulePositionConfig(x=5, y=15)
    module = ModuleConfig(
        name="TestModule",
        module_type="Clock",
        position=position,
        refresh_interval=1000,
        arguments={"key": "value"},
    )
    assert module.name == "TestModule"
    assert module.module_type == "Clock"
    assert module.position == position
    assert module.refresh_interval == 1000
    assert module.arguments == {"key": "value"}


def test_module_config_default_arguments():
    """Test ModuleConfig with default arguments."""
    position = ModulePositionConfig(x=0, y=0)
    module = ModuleConfig(
        name="DefaultModule",
        module_type="DefaultType",
        position=position,
        refresh_interval=500,
    )
    assert module.arguments == {}


def test_scene_config():
    """Test initialization of SceneConfig."""
    scene = SceneConfig(
        name="TestScene",
        show_for=10,
        scene_order=1,
        modules=["Module1", "Module2"],
    )
    assert scene.name == "TestScene"
    assert scene.show_for == 10
    assert scene.scene_order == 1
    assert scene.modules == ["Module1", "Module2"]


def test_device_config():
    """Test initialization of DeviceConfig."""
    position = ModulePositionConfig(x=0, y=0)
    module = ModuleConfig(
        name="TestModule",
        module_type="Clock",
        position=position,
        refresh_interval=1000,
    )
    scene = SceneConfig(
        name="TestScene",
        show_for=10,
        scene_order=1,
        modules=["Module1"],
    )
    device = DeviceConfig(
        name="TestDevice",
        device_address="192.168.1.1",
        speed=9600,
        brightness=255,
        on_bytes=1,
        off_bytes=0,
        modules=[module],
        scenes=[scene],
    )
    assert device.name == "TestDevice"
    assert device.location == "192.168.1.1"
    assert device.speed == 9600
    assert device.brightness == 255
    assert device.on_bytes == 1
    assert device.off_bytes == 0
    assert device.modules == [module]
    assert device.scenes == [scene]


def test_config():
    """Test initialization of Config."""
    position = ModulePositionConfig(x=0, y=0)
    module = ModuleConfig(
        name="TestModule",
        module_type="Clock",
        position=position,
        refresh_interval=1000,
    )
    scene = SceneConfig(
        name="TestScene",
        show_for=10,
        scene_order=1,
        modules=["Module1"],
    )
    device = DeviceConfig(
        name="TestDevice",
        device_address="192.168.1.1",
        speed=9600,
        brightness=255,
        on_bytes=1,
        off_bytes=0,
        modules=[module],
        scenes=[scene],
    )
    config = Config(devices=[device])
    assert config.devices == [device]
