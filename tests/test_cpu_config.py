import pytest
from marshmallow import ValidationError
from flem.models.modules.cpu_config import (
    CpuConfigArguments,
    CpuConfig,
    CpuConfigArgumentsSchema,
    CpuConfigSchema,
)
from flem.models.config import ModulePositionConfig


def test_cpu_config_arguments_initialization():
    """Test the initialization of CpuConfigArguments."""
    arguments = CpuConfigArguments(
        temp_sensor="coretemp",
        temp_sensor_index=0,
        show_temp=True,
        use_bar_graph=True,
    )

    assert arguments.temp_sensor == "coretemp"
    assert arguments.temp_sensor_index == 0
    assert arguments.show_temp is True
    assert arguments.use_bar_graph is True


def test_cpu_config_arguments_default_values():
    """Test the default values of CpuConfigArguments."""
    arguments = CpuConfigArguments(temp_sensor="coretemp", temp_sensor_index=1)

    assert arguments.temp_sensor == "coretemp"
    assert arguments.temp_sensor_index == 1
    assert arguments.show_temp is False
    assert arguments.use_bar_graph is False


def test_cpu_config_initialization():
    """Test the initialization of CpuConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = CpuConfigArguments(
        temp_sensor="coretemp",
        temp_sensor_index=0,
        show_temp=True,
        use_bar_graph=False,
    )

    config = CpuConfig(
        name="TestCpu",
        module_type="Cpu",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )

    assert config.name == "TestCpu"
    assert config.module_type == "Cpu"
    assert config.position == position
    assert config.refresh_interval == 1000
    assert config.arguments == arguments


def test_cpu_config_arguments_schema_load():
    """Test loading data into CpuConfigArguments using CpuConfigArgumentsSchema."""
    data = {
        "temp_sensor": "coretemp",
        "temp_sensor_index": 0,
        "show_temp": True,
        "use_bar_graph": False,
    }
    schema = CpuConfigArgumentsSchema()
    result = schema.load(data)

    assert isinstance(result, CpuConfigArguments)
    assert result.temp_sensor == "coretemp"
    assert result.temp_sensor_index == 0
    assert result.show_temp is True
    assert result.use_bar_graph is False


def test_cpu_config_arguments_schema_dump():
    """Test dumping CpuConfigArguments data using CpuConfigArgumentsSchema."""
    arguments = CpuConfigArguments(
        temp_sensor="coretemp",
        temp_sensor_index=1,
        show_temp=False,
        use_bar_graph=True,
    )
    schema = CpuConfigArgumentsSchema()
    result = schema.dump(arguments)

    assert result == {
        "temp_sensor": "coretemp",
        "temp_sensor_index": 1,
        "show_temp": False,
        "use_bar_graph": True,
    }


def test_cpu_config_schema_load():
    """Test loading data into CpuConfig using CpuConfigSchema."""
    data = {
        "name": "TestCpu",
        "module_type": "Cpu",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {
            "temp_sensor": "coretemp",
            "temp_sensor_index": 0,
            "show_temp": True,
            "use_bar_graph": False,
        },
    }
    schema = CpuConfigSchema()
    result = schema.load(data)

    assert isinstance(result, CpuConfig)
    assert result.name == "TestCpu"
    assert result.module_type == "Cpu"
    assert result.position.x == 0
    assert result.position.y == 0
    assert result.refresh_interval == 1000
    assert result.arguments.temp_sensor == "coretemp"
    assert result.arguments.temp_sensor_index == 0
    assert result.arguments.show_temp is True
    assert result.arguments.use_bar_graph is False


def test_cpu_config_schema_dump():
    """Test dumping CpuConfig data using CpuConfigSchema."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = CpuConfigArguments(
        temp_sensor="coretemp",
        temp_sensor_index=1,
        show_temp=False,
        use_bar_graph=True,
    )
    config = CpuConfig(
        name="TestCpu",
        module_type="Cpu",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )
    schema = CpuConfigSchema()
    result = schema.dump(config)

    assert result == {
        "name": "TestCpu",
        "module_type": "Cpu",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {
            "temp_sensor": "coretemp",
            "temp_sensor_index": 1,
            "show_temp": False,
            "use_bar_graph": True,
        },
    }
