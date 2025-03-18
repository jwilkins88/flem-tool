import pytest
from marshmallow import ValidationError
from flem.models.config import ModulePositionConfig
from flem.models.modules.battery_config import (
    BatteryConfigArgumentsSchema,
    BatteryConfigArguments,
    BatteryConfigSchema,
    BatteryConfig,
)


def test_battery_config_arguments_schema_make_module():
    """Test BatteryConfigArgumentsSchema's make_module method."""
    schema = BatteryConfigArgumentsSchema()
    data = {"show_percentage": True}

    result = schema.load(data)

    assert isinstance(result, BatteryConfigArguments)
    assert result.show_percentage is True


def test_battery_config_arguments_schema_make_module_default():
    """Test BatteryConfigArgumentsSchema's make_module method with default values."""
    schema = BatteryConfigArgumentsSchema()
    data = {}

    result = schema.load(data)

    assert isinstance(result, BatteryConfigArguments)
    assert result.show_percentage is False


def test_battery_config_arguments_schema_make_module_invalid():
    """Test BatteryConfigArgumentsSchema's make_module method with invalid data."""
    schema = BatteryConfigArgumentsSchema()
    data = {"show_percentage": "invalid_value"}

    with pytest.raises(ValidationError):
        schema.load(data)


def test_clock_config_schema_make_module():
    """Test ClockConfigSchema's make_module method."""
    schema = BatteryConfigSchema()
    data = {
        "name": "BatteryModule",
        "module_type": "Battery",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {"show_percentage": True},
    }

    result = schema.load(data)

    assert isinstance(result, BatteryConfig)
    assert result.name == "BatteryModule"
    assert result.module_type == "Battery"
    assert isinstance(result.position, ModulePositionConfig)
    assert result.position.x == 0
    assert result.position.y == 0
    assert result.refresh_interval == 1000
    assert isinstance(result.arguments, BatteryConfigArguments)
    assert result.arguments.show_percentage is True


def test_clock_config_schema_make_module_invalid():
    """Test ClockConfigSchema's make_module method with invalid data."""
    schema = BatteryConfigSchema()
    data = {
        "name": "BatteryModule",
        "module_type": "Battery",
        "position": {"x": "invalid", "y": 0},
        "refresh_interval": 1000,
        "arguments": {"show_percentage": True},
    }

    with pytest.raises(ValidationError):
        schema.load(data)


def test_battery_config_arguments_schema():
    """Test the BatteryConfigArgumentsSchema mapping."""
    schema = BatteryConfigArgumentsSchema()

    # Input data
    input_data = {
        "show_percentage": True,
        "critical_threshold": 15,
    }

    # Deserialize input data
    result = schema.load(input_data)

    # Verify the result is a BatteryConfigArguments object
    assert isinstance(result, BatteryConfigArguments)
    assert result.show_percentage is True
    assert result.critical_threshold == 15


def test_battery_config_arguments_schema_defaults():
    """Test the BatteryConfigArgumentsSchema with default values."""
    schema = BatteryConfigArgumentsSchema()

    # Input data with no fields provided
    input_data = {}

    # Deserialize input data
    result = schema.load(input_data)

    # Verify the result is a BatteryConfigArguments object with default values
    assert isinstance(result, BatteryConfigArguments)
    assert result.show_percentage is False
    assert result.critical_threshold == 20  # Default value


def test_battery_config_schema():
    """Test the BatteryConfigSchema mapping."""
    schema = BatteryConfigSchema()

    # Input data
    input_data = {
        "name": "BatteryModule",
        "module_type": "Battery",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {
            "show_percentage": True,
            "critical_threshold": 15,
        },
    }

    # Deserialize input data
    result = schema.load(input_data)

    # Verify the result is a BatteryConfig object
    assert isinstance(result, BatteryConfig)
    assert result.name == "BatteryModule"
    assert result.module_type == "Battery"
    assert isinstance(result.position, ModulePositionConfig)
    assert result.position.x == 0
    assert result.position.y == 0
    assert result.refresh_interval == 1000
    assert isinstance(result.arguments, BatteryConfigArguments)
    assert result.arguments.show_percentage is True
    assert result.arguments.critical_threshold == 15


def test_battery_config_schema_defaults():
    """Test the BatteryConfigSchema with default argument values."""
    schema = BatteryConfigSchema()

    # Input data with no arguments provided
    input_data = {
        "name": "BatteryModule",
        "module_type": "Battery",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {},
    }

    # Deserialize input data
    result = schema.load(input_data)

    # Verify the result is a BatteryConfig object with default argument values
    assert isinstance(result, BatteryConfig)
    assert result.name == "BatteryModule"
    assert result.module_type == "Battery"
    assert isinstance(result.position, ModulePositionConfig)
    assert result.position.x == 0
    assert result.position.y == 0
    assert result.refresh_interval == 1000
    assert isinstance(result.arguments, BatteryConfigArguments)
    assert result.arguments.show_percentage is False  # Default value
    assert result.arguments.critical_threshold == 20  # Default value
