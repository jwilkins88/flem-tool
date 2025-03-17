import pytest
from marshmallow import ValidationError
from flem.models.modules.line_config import (
    LineConfigArguments,
    LineConfig,
    LineConfigArgumentsSchema,
    LineConfigSchema,
)
from flem.models.config import ModulePositionConfig


def test_line_config_arguments_initialization():
    """Test the initialization of LineConfigArguments."""
    arguments = LineConfigArguments(line_style="dashed", width=5)

    assert arguments.line_style == "dashed"
    assert arguments.width == 5


def test_line_config_arguments_invalid_line_style():
    """Test LineConfigArguments with an invalid line style."""
    arguments = LineConfigArguments(line_style="invalid", width=3)

    assert arguments.line_style == "invalid"
    assert arguments.width == 3


def test_line_config_initialization():
    """Test the initialization of LineConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = LineConfigArguments(line_style="solid", width=10)

    config = LineConfig(
        name="TestLine",
        module_type="Line",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )

    assert config.name == "TestLine"
    assert config.module_type == "Line"
    assert config.position == position
    assert config.refresh_interval == 1000
    assert config.arguments == arguments


def test_line_config_invalid_line_style():
    """Test LineConfig with an invalid line style."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = LineConfigArguments(line_style="invalid", width=5)

    config = LineConfig(
        name="TestLine",
        module_type="Line",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )
    assert config.arguments.line_style == "solid"


def test_line_config_arguments_schema_load():
    """Test loading data into LineConfigArguments using LineConfigArgumentsSchema."""
    data = {"line_style": "solid", "width": 5}
    schema = LineConfigArgumentsSchema()
    result = schema.load(data)

    assert isinstance(result, LineConfigArguments)
    assert result.line_style == "solid"
    assert result.width == 5


def test_line_config_arguments_schema_dump():
    """Test dumping LineConfigArguments data using LineConfigArgumentsSchema."""
    arguments = LineConfigArguments(line_style="dashed", width=3)
    schema = LineConfigArgumentsSchema()
    result = schema.dump(arguments)

    assert result == {"line_style": "dashed", "width": 3}


def test_line_config_schema_load():
    """Test loading data into LineConfig using LineConfigSchema."""
    data = {
        "name": "TestLine",
        "module_type": "Line",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {"line_style": "solid", "width": 5},
    }
    schema = LineConfigSchema()
    result = schema.load(data)

    assert isinstance(result, LineConfig)
    assert result.name == "TestLine"
    assert result.module_type == "Line"
    assert result.position.x == 0
    assert result.position.y == 0
    assert result.refresh_interval == 1000
    assert result.arguments.line_style == "solid"
    assert result.arguments.width == 5


def test_line_config_schema_dump():
    """Test dumping LineConfig data using LineConfigSchema."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = LineConfigArguments(line_style="dashed", width=3)
    config = LineConfig(
        name="TestLine",
        module_type="Line",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )
    schema = LineConfigSchema()
    result = schema.dump(config)

    assert result == {
        "name": "TestLine",
        "module_type": "Line",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {"line_style": "dashed", "width": 3},
    }
