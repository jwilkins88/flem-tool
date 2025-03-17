import pytest
from flem.models.config_schema import (
    ModulePositionSchema,
    ModuleSchema,
    SceneSchema,
    DeviceSchema,
    ConfigSchema,
)
from flem.models.config import (
    ModulePositionConfig,
    ModuleConfig,
    SceneConfig,
    DeviceConfig,
    Config,
)


def test_module_position_schema_load():
    """Test loading data into ModulePositionConfig using ModulePositionSchema."""
    data = {"x": 5, "y": 10}
    schema = ModulePositionSchema()
    result = schema.load(data)

    assert isinstance(result, ModulePositionConfig)
    assert result.x == 5
    assert result.y == 10


def test_module_position_schema_dump():
    """Test dumping ModulePositionConfig data using ModulePositionSchema."""
    position = ModulePositionConfig(x=5, y=10)
    schema = ModulePositionSchema()
    result = schema.dump(position)

    assert result == {"x": 5, "y": 10}


def test_module_schema_load():
    """Test loading data into ModuleConfig using ModuleSchema."""
    data = {
        "name": "TestModule",
        "module_type": "TestType",
        "position": {"x": 5, "y": 10},
        "refresh_interval": 1000,
        "arguments": {"key": "value"},
    }
    schema = ModuleSchema()
    result = schema.load(data)

    assert isinstance(result, ModuleConfig)
    assert result.name == "TestModule"
    assert result.module_type == "TestType"
    assert result.position.x == 5
    assert result.position.y == 10
    assert result.refresh_interval == 1000
    assert result.arguments == {"key": "value"}


def test_module_schema_dump():
    """Test dumping ModuleConfig data using ModuleSchema."""
    position = ModulePositionConfig(x=5, y=10)
    module = ModuleConfig(
        name="TestModule",
        module_type="TestType",
        position=position,
        refresh_interval=1000,
        arguments={"key": "value"},
    )
    schema = ModuleSchema()
    result = schema.dump(module)

    assert result == {
        "name": "TestModule",
        "module_type": "TestType",
        "position": {"x": 5, "y": 10},
        "refresh_interval": 1000,
        "arguments": {"key": "value"},
    }


def test_scene_schema_load():
    """Test loading data into SceneConfig using SceneSchema."""
    data = {
        "name": "TestScene",
        "show_for": 10,
        "scene_order": 1,
        "modules": ["Module1", "Module2"],
    }
    schema = SceneSchema()
    result = schema.load(data)

    assert isinstance(result, SceneConfig)
    assert result.name == "TestScene"
    assert result.show_for == 10
    assert result.scene_order == 1
    assert result.modules == ["Module1", "Module2"]


def test_scene_schema_dump():
    """Test dumping SceneConfig data using SceneSchema."""
    scene = SceneConfig(
        name="TestScene",
        show_for=10,
        scene_order=1,
        modules=["Module1", "Module2"],
    )
    schema = SceneSchema()
    result = schema.dump(scene)

    assert result == {
        "name": "TestScene",
        "show_for": 10,
        "scene_order": 1,
        "modules": ["Module1", "Module2"],
    }


def test_device_schema_load():
    """Test loading data into DeviceConfig using DeviceSchema."""
    data = {
        "name": "TestDevice",
        "device_address": "192.168.1.1",
        "speed": 9600,
        "brightness": 255,
        "on_bytes": 1,
        "off_bytes": 0,
        "modules": [
            {
                "name": "TestModule",
                "module_type": "TestType",
                "position": {"x": 5, "y": 10},
                "refresh_interval": 1000,
                "arguments": {"key": "value"},
            }
        ],
        "scenes": [
            {
                "name": "TestScene",
                "show_for": 10,
                "scene_order": 1,
                "modules": ["Module1", "Module2"],
            }
        ],
    }
    schema = DeviceSchema()
    result = schema.load(data)

    assert isinstance(result, DeviceConfig)
    assert result.name == "TestDevice"
    assert result.device_address == "192.168.1.1"
    assert result.speed == 9600
    assert result.brightness == 255
    assert result.on_bytes == 1
    assert result.off_bytes == 0
    assert len(result.modules) == 1
    assert result.modules[0].name == "TestModule"
    assert len(result.scenes) == 1
    assert result.scenes[0].name == "TestScene"


def test_device_schema_dump():
    """Test dumping DeviceConfig data using DeviceSchema."""
    position = ModulePositionConfig(x=5, y=10)
    module = ModuleConfig(
        name="TestModule",
        module_type="TestType",
        position=position,
        refresh_interval=1000,
        arguments={"key": "value"},
    )
    scene = SceneConfig(
        name="TestScene",
        show_for=10,
        scene_order=1,
        modules=["Module1", "Module2"],
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
    schema = DeviceSchema()
    result = schema.dump(device)

    assert result == {
        "name": "TestDevice",
        "device_address": "192.168.1.1",
        "speed": 9600,
        "brightness": 255,
        "on_bytes": 1,
        "off_bytes": 0,
        "modules": [
            {
                "name": "TestModule",
                "module_type": "TestType",
                "position": {"x": 5, "y": 10},
                "refresh_interval": 1000,
                "arguments": {"key": "value"},
            }
        ],
        "scenes": [
            {
                "name": "TestScene",
                "show_for": 10,
                "scene_order": 1,
                "modules": ["Module1", "Module2"],
            }
        ],
    }


def test_config_schema_load():
    """Test loading data into Config using ConfigSchema."""
    data = {
        "devices": [
            {
                "name": "TestDevice",
                "device_address": "192.168.1.1",
                "speed": 9600,
                "brightness": 255,
                "on_bytes": 1,
                "off_bytes": 0,
                "modules": [
                    {
                        "name": "TestModule",
                        "module_type": "TestType",
                        "position": {"x": 5, "y": 10},
                        "refresh_interval": 1000,
                        "arguments": {"key": "value"},
                    }
                ],
                "scenes": [
                    {
                        "name": "TestScene",
                        "show_for": 10,
                        "scene_order": 1,
                        "modules": ["Module1", "Module2"],
                    }
                ],
            }
        ]
    }
    schema = ConfigSchema()
    result = schema.load(data)

    assert isinstance(result, Config)
    assert len(result.devices) == 1
    assert result.devices[0].name == "TestDevice"


def test_config_schema_dump():
    """Test dumping Config data using ConfigSchema."""
    position = ModulePositionConfig(x=5, y=10)
    module = ModuleConfig(
        name="TestModule",
        module_type="TestType",
        position=position,
        refresh_interval=1000,
        arguments={"key": "value"},
    )
    scene = SceneConfig(
        name="TestScene",
        show_for=10,
        scene_order=1,
        modules=["Module1", "Module2"],
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
    schema = ConfigSchema()
    result = schema.dump(config)

    assert result == {
        "devices": [
            {
                "name": "TestDevice",
                "device_address": "192.168.1.1",
                "speed": 9600,
                "brightness": 255,
                "on_bytes": 1,
                "off_bytes": 0,
                "modules": [
                    {
                        "name": "TestModule",
                        "module_type": "TestType",
                        "position": {"x": 5, "y": 10},
                        "refresh_interval": 1000,
                        "arguments": {"key": "value"},
                    }
                ],
                "scenes": [
                    {
                        "name": "TestScene",
                        "show_for": 10,
                        "scene_order": 1,
                        "modules": ["Module1", "Module2"],
                    }
                ],
            }
        ]
    }
