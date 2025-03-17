import pytest
from marshmallow import ValidationError
from flem.models.modules.clock_config import (
    ClockConfigArguments,
    ClockConfig,
    ClockConfigArgumentsSchema,
    ClockConfigSchema,
)
from flem.models.config import ModulePositionConfig


def test_clock_config_arguments_initialization():
    """Test the initialization of ClockConfigArguments."""
    arguments = ClockConfigArguments(clock_mode="12h", show_seconds_indicator=True)

    assert arguments.clock_mode == "12h"
    assert arguments.show_seconds_indicator is True


def test_clock_config_arguments_default_values():
    """Test the default values of ClockConfigArguments."""
    arguments = ClockConfigArguments(clock_mode="24h")

    assert arguments.clock_mode == "24h"
    assert arguments.show_seconds_indicator is False


def test_clock_config_initialization():
    """Test the initialization of ClockConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = ClockConfigArguments(clock_mode="12h", show_seconds_indicator=True)

    config = ClockConfig(
        name="TestClock",
        module_type="Clock",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )

    assert config.name == "TestClock"
    assert config.module_type == "Clock"
    assert config.position == position
    assert config.refresh_interval == 1000
    assert config.arguments == arguments


def test_clock_config_invalid_clock_mode():
    """Test ClockConfig with an invalid clock mode."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = ClockConfigArguments(
        clock_mode="invalid_mode", show_seconds_indicator=True
    )
    config = ClockConfig(
        name="TestClock",
        module_type="Clock",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )

    assert config.arguments.clock_mode == "12h"


def test_clock_config_arguments_schema_load():
    """Test loading data into ClockConfigArguments using ClockConfigArgumentsSchema."""
    data = {"clock_mode": "12h", "show_seconds_indicator": True}
    schema = ClockConfigArgumentsSchema()
    result = schema.load(data)

    assert isinstance(result, ClockConfigArguments)
    assert result.clock_mode == "12h"
    assert result.show_seconds_indicator is True


def test_clock_config_arguments_schema_dump():
    """Test dumping ClockConfigArguments data using ClockConfigArgumentsSchema."""
    arguments = ClockConfigArguments(clock_mode="24h", show_seconds_indicator=False)
    schema = ClockConfigArgumentsSchema()
    result = schema.dump(arguments)

    assert result == {"clock_mode": "24h", "show_seconds_indicator": False}


def test_clock_config_schema_load():
    """Test loading data into ClockConfig using ClockConfigSchema."""
    data = {
        "name": "TestClock",
        "module_type": "Clock",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {"clock_mode": "12h", "show_seconds_indicator": True},
    }
    schema = ClockConfigSchema()
    result = schema.load(data)

    assert isinstance(result, ClockConfig)
    assert result.name == "TestClock"
    assert result.module_type == "Clock"
    assert result.position.x == 0
    assert result.position.y == 0
    assert result.refresh_interval == 1000
    assert result.arguments.clock_mode == "12h"
    assert result.arguments.show_seconds_indicator is True


def test_clock_config_schema_dump():
    """Test dumping ClockConfig data using ClockConfigSchema."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = ClockConfigArguments(clock_mode="24h", show_seconds_indicator=False)
    config = ClockConfig(
        name="TestClock",
        module_type="Clock",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )
    schema = ClockConfigSchema()
    result = schema.dump(config)

    assert result == {
        "name": "TestClock",
        "module_type": "Clock",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {"clock_mode": "24h", "show_seconds_indicator": False},
    }
