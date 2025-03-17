import pytest
from marshmallow import ValidationError
from flem.models.modules.gpu_config import (
    GpuConfigArguments,
    GpuConfig,
    GpuConfigArgumentsSchema,
    GpuConfigSchema,
)
from flem.models.config import ModulePositionConfig


def test_gpu_config_arguments_initialization():
    """Test the initialization of GpuConfigArguments."""
    arguments = GpuConfigArguments(
        gpu_command="nvidia-smi",
        gpu_command_arguments=["--query-gpu=temperature.gpu", "--format=csv"],
        gpu_index=0,
        gpu_temp_property="temperature.gpu",
        gpu_util_property="utilization.gpu",
        show_temp=True,
        use_bar_graph=True,
    )

    assert arguments.gpu_command == "nvidia-smi"
    assert arguments.gpu_command_arguments == [
        "--query-gpu=temperature.gpu",
        "--format=csv",
    ]
    assert arguments.gpu_index == 0
    assert arguments.gpu_temp_property == "temperature.gpu"
    assert arguments.gpu_util_property == "utilization.gpu"
    assert arguments.show_temp is True
    assert arguments.use_bar_graph is True


def test_gpu_config_arguments_default_values():
    """Test the default values of GpuConfigArguments."""
    arguments = GpuConfigArguments(
        gpu_command="nvidia-smi",
        gpu_command_arguments=["--query-gpu=temperature.gpu", "--format=csv"],
        gpu_index=1,
        gpu_temp_property="temperature.gpu",
        gpu_util_property="utilization.gpu",
    )

    assert arguments.gpu_command == "nvidia-smi"
    assert arguments.gpu_command_arguments == [
        "--query-gpu=temperature.gpu",
        "--format=csv",
    ]
    assert arguments.gpu_index == 1
    assert arguments.gpu_temp_property == "temperature.gpu"
    assert arguments.gpu_util_property == "utilization.gpu"
    assert arguments.show_temp is False
    assert arguments.use_bar_graph is False


def test_gpu_config_initialization():
    """Test the initialization of GpuConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = GpuConfigArguments(
        gpu_command="nvidia-smi",
        gpu_command_arguments=["--query-gpu=temperature.gpu", "--format=csv"],
        gpu_index=0,
        gpu_temp_property="temperature.gpu",
        gpu_util_property="utilization.gpu",
        show_temp=True,
        use_bar_graph=False,
    )

    config = GpuConfig(
        name="TestGpu",
        module_type="Gpu",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )

    assert config.name == "TestGpu"
    assert config.module_type == "Gpu"
    assert config.position == position
    assert config.refresh_interval == 1000
    assert config.arguments == arguments


def test_gpu_config_arguments_schema_load():
    """Test loading data into GpuConfigArguments using GpuConfigArgumentsSchema."""
    data = {
        "gpu_command": "nvidia-smi",
        "gpu_command_arguments": ["--query-gpu=temperature.gpu", "--format=csv"],
        "gpu_index": 0,
        "gpu_temp_property": "temperature.gpu",
        "gpu_util_property": "utilization.gpu",
        "show_temp": True,
        "use_bar_graph": False,
    }
    schema = GpuConfigArgumentsSchema()
    result = schema.load(data)

    assert isinstance(result, GpuConfigArguments)
    assert result.gpu_command == "nvidia-smi"
    assert result.gpu_command_arguments == [
        "--query-gpu=temperature.gpu",
        "--format=csv",
    ]
    assert result.gpu_index == 0
    assert result.gpu_temp_property == "temperature.gpu"
    assert result.gpu_util_property == "utilization.gpu"
    assert result.show_temp is True
    assert result.use_bar_graph is False


def test_gpu_config_arguments_schema_dump():
    """Test dumping GpuConfigArguments data using GpuConfigArgumentsSchema."""
    arguments = GpuConfigArguments(
        gpu_command="nvidia-smi",
        gpu_command_arguments=["--query-gpu=temperature.gpu", "--format=csv"],
        gpu_index=0,
        gpu_temp_property="temperature.gpu",
        gpu_util_property="utilization.gpu",
        show_temp=True,
        use_bar_graph=False,
    )
    schema = GpuConfigArgumentsSchema()
    result = schema.dump(arguments)

    assert result == {
        "gpu_command": "nvidia-smi",
        "gpu_command_arguments": ["--query-gpu=temperature.gpu", "--format=csv"],
        "gpu_index": 0,
        "gpu_temp_property": "temperature.gpu",
        "gpu_util_property": "utilization.gpu",
        "show_temp": True,
        "use_bar_graph": False,
    }


def test_gpu_config_schema_load():
    """Test loading data into GpuConfig using GpuConfigSchema."""
    data = {
        "name": "TestGpu",
        "module_type": "Gpu",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {
            "gpu_command": "nvidia-smi",
            "gpu_command_arguments": ["--query-gpu=temperature.gpu", "--format=csv"],
            "gpu_index": 0,
            "gpu_temp_property": "temperature.gpu",
            "gpu_util_property": "utilization.gpu",
            "show_temp": True,
            "use_bar_graph": False,
        },
    }
    schema = GpuConfigSchema()
    result = schema.load(data)

    assert isinstance(result, GpuConfig)
    assert result.name == "TestGpu"
    assert result.module_type == "Gpu"
    assert result.position.x == 0
    assert result.position.y == 0
    assert result.refresh_interval == 1000
    assert result.arguments.gpu_command == "nvidia-smi"
    assert result.arguments.gpu_command_arguments == [
        "--query-gpu=temperature.gpu",
        "--format=csv",
    ]
    assert result.arguments.gpu_index == 0
    assert result.arguments.gpu_temp_property == "temperature.gpu"
    assert result.arguments.gpu_util_property == "utilization.gpu"
    assert result.arguments.show_temp is True
    assert result.arguments.use_bar_graph is False


def test_gpu_config_schema_dump():
    """Test dumping GpuConfig data using GpuConfigSchema."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = GpuConfigArguments(
        gpu_command="nvidia-smi",
        gpu_command_arguments=["--query-gpu=temperature.gpu", "--format=csv"],
        gpu_index=0,
        gpu_temp_property="temperature.gpu",
        gpu_util_property="utilization.gpu",
        show_temp=True,
        use_bar_graph=False,
    )
    config = GpuConfig(
        name="TestGpu",
        module_type="Gpu",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )
    schema = GpuConfigSchema()
    result = schema.dump(config)

    assert result == {
        "name": "TestGpu",
        "module_type": "Gpu",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {
            "gpu_command": "nvidia-smi",
            "gpu_command_arguments": ["--query-gpu=temperature.gpu", "--format=csv"],
            "gpu_index": 0,
            "gpu_temp_property": "temperature.gpu",
            "gpu_util_property": "utilization.gpu",
            "show_temp": True,
            "use_bar_graph": False,
        },
    }
