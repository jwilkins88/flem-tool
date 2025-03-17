import pytest
from marshmallow import ValidationError
from flem.models.modules.weather_config import (
    WeatherConfigArguments,
    WeatherConfig,
    WeatherConfigArgumentsSchema,
    WeatherConfigSchema,
)
from flem.models.config import ModulePositionConfig


def test_weather_config_arguments_initialization():
    """Test the initialization of WeatherConfigArguments."""
    arguments = WeatherConfigArguments(
        api_url="https://api.openweathermap.org/data/2.5/weather",
        api_key="test_api_key",
        city_id=12345,
        temperature_unit="Celsius",
        show_wind_speed=True,
        show_humidity=True,
        response_temperature_property="main.temp",
        response_icon_property="weather[0].icon",
        response_wind_speed_property="wind.speed",
        response_wind_direction_property="wind.deg",
        response_humidity_property="main.humidity",
    )

    assert arguments.api_url == "https://api.openweathermap.org/data/2.5/weather"
    assert arguments.api_key == "test_api_key"
    assert arguments.city_id == 12345
    assert arguments.temperature_unit == "Celsius"
    assert arguments.show_wind_speed is True
    assert arguments.show_humidity is True
    assert arguments.response_temperature_property == "main.temp"
    assert arguments.response_icon_property == "weather[0].icon"
    assert arguments.response_wind_speed_property == "wind.speed"
    assert arguments.response_wind_direction_property == "wind.deg"
    assert arguments.response_humidity_property == "main.humidity"


def test_weather_config_arguments_default_values():
    """Test the default values of WeatherConfigArguments."""
    arguments = WeatherConfigArguments(
        api_url="https://api.openweathermap.org/data/2.5/weather",
        api_key="test_api_key",
        city_id=12345,
    )

    assert arguments.api_url == "https://api.openweathermap.org/data/2.5/weather"
    assert arguments.api_key == "test_api_key"
    assert arguments.city_id == 12345
    assert arguments.temperature_unit is None
    assert arguments.show_wind_speed is False
    assert arguments.show_humidity is False
    assert arguments.response_temperature_property is None
    assert arguments.response_icon_property is None
    assert arguments.response_wind_speed_property is None
    assert arguments.response_wind_direction_property is None
    assert arguments.response_humidity_property is None


def test_weather_config_initialization():
    """Test the initialization of WeatherConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = WeatherConfigArguments(
        api_url="https://api.openweathermap.org/data/2.5/weather",
        api_key="test_api_key",
        city_id=12345,
        temperature_unit="Celsius",
    )

    config = WeatherConfig(
        name="TestWeather",
        module_type="Weather",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )

    assert config.name == "TestWeather"
    assert config.module_type == "Weather"
    assert config.position == position
    assert config.refresh_interval == 1000
    assert config.arguments == arguments


def test_weather_config_invalid_temperature_unit():
    """Test WeatherConfig with an invalid temperature unit."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = WeatherConfigArguments(
        api_url="https://api.openweathermap.org/data/2.5/weather",
        api_key="test_api_key",
        city_id=12345,
        temperature_unit=None,
    )

    with pytest.raises(ValueError, match="Invalid temperature unit"):
        WeatherConfig(
            name="TestWeather",
            module_type="Weather",
            position=position,
            refresh_interval=1000,
            arguments=arguments,
        )


def test_weather_config_arguments_schema_load():
    """Test loading data into WeatherConfigArguments using WeatherConfigArgumentsSchema."""
    data = {
        "api_url": "https://api.openweathermap.org/data/2.5/weather",
        "api_key": "test_api_key",
        "city_id": 12345,
        "temperature_unit": "Celsius",
        "show_wind_speed": True,
        "show_humidity": True,
        "response_temperature_property": "main.temp",
        "response_icon_property": "weather[0].icon",
        "response_wind_speed_property": "wind.speed",
        "response_wind_direction_property": "wind.deg",
        "response_humidity_property": "main.humidity",
    }
    schema = WeatherConfigArgumentsSchema()
    result = schema.load(data)

    assert isinstance(result, WeatherConfigArguments)
    assert result.api_url == "https://api.openweathermap.org/data/2.5/weather"
    assert result.api_key == "test_api_key"
    assert result.city_id == 12345
    assert result.temperature_unit == "Celsius"
    assert result.show_wind_speed is True
    assert result.show_humidity is True
    assert result.response_temperature_property == "main.temp"
    assert result.response_icon_property == "weather[0].icon"
    assert result.response_wind_speed_property == "wind.speed"
    assert result.response_wind_direction_property == "wind.deg"
    assert result.response_humidity_property == "main.humidity"


def test_weather_config_arguments_schema_dump():
    """Test dumping WeatherConfigArguments data using WeatherConfigArgumentsSchema."""
    arguments = WeatherConfigArguments(
        api_url="https://api.openweathermap.org/data/2.5/weather",
        api_key="test_api_key",
        city_id=12345,
        temperature_unit="Celsius",
        show_wind_speed=True,
        show_humidity=True,
        response_temperature_property="main.temp",
        response_icon_property="weather[0].icon",
        response_wind_speed_property="wind.speed",
        response_wind_direction_property="wind.deg",
        response_humidity_property="main.humidity",
    )
    schema = WeatherConfigArgumentsSchema()
    result = schema.dump(arguments)

    assert result == {
        "api_url": "https://api.openweathermap.org/data/2.5/weather",
        "api_key": "test_api_key",
        "city_id": 12345,
        "temperature_unit": "Celsius",
        "show_wind_speed": True,
        "show_humidity": True,
        "response_temperature_property": "main.temp",
        "response_icon_property": "weather[0].icon",
        "response_wind_speed_property": "wind.speed",
        "response_wind_direction_property": "wind.deg",
        "response_humidity_property": "main.humidity",
    }


def test_weather_config_schema_load():
    """Test loading data into WeatherConfig using WeatherConfigSchema."""
    data = {
        "name": "TestWeather",
        "module_type": "Weather",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {
            "api_url": "https://api.openweathermap.org/data/2.5/weather",
            "api_key": "test_api_key",
            "city_id": 12345,
            "temperature_unit": "Celsius",
            "show_wind_speed": True,
            "show_humidity": True,
            "response_temperature_property": "main.temp",
            "response_icon_property": "weather[0].icon",
            "response_wind_speed_property": "wind.speed",
            "response_wind_direction_property": "wind.deg",
            "response_humidity_property": "main.humidity",
        },
    }
    schema = WeatherConfigSchema()
    result = schema.load(data)

    assert isinstance(result, WeatherConfig)
    assert result.name == "TestWeather"
    assert result.module_type == "Weather"
    assert result.position.x == 0
    assert result.position.y == 0
    assert result.refresh_interval == 1000
    assert result.arguments.api_url == "https://api.openweathermap.org/data/2.5/weather"
    assert result.arguments.api_key == "test_api_key"
    assert result.arguments.city_id == 12345
    assert result.arguments.temperature_unit == "Celsius"
    assert result.arguments.show_wind_speed is True
    assert result.arguments.show_humidity is True
    assert result.arguments.response_temperature_property == "main.temp"
    assert result.arguments.response_icon_property == "weather[0].icon"
    assert result.arguments.response_wind_speed_property == "wind.speed"
    assert result.arguments.response_wind_direction_property == "wind.deg"
    assert result.arguments.response_humidity_property == "main.humidity"


def test_weather_config_schema_dump():
    """Test dumping WeatherConfig data using WeatherConfigSchema."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = WeatherConfigArguments(
        api_url="https://api.openweathermap.org/data/2.5/weather",
        api_key="test_api_key",
        city_id=12345,
        temperature_unit="Celsius",
        show_wind_speed=True,
        show_humidity=True,
        response_temperature_property="main.temp",
        response_icon_property="weather[0].icon",
        response_wind_speed_property="wind.speed",
        response_wind_direction_property="wind.deg",
        response_humidity_property="main.humidity",
    )
    config = WeatherConfig(
        name="TestWeather",
        module_type="Weather",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )
    schema = WeatherConfigSchema()
    result = schema.dump(config)

    assert result == {
        "name": "TestWeather",
        "module_type": "Weather",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {
            "api_url": "https://api.openweathermap.org/data/2.5/weather",
            "api_key": "test_api_key",
            "city_id": 12345,
            "temperature_unit": "Celsius",
            "show_wind_speed": True,
            "show_humidity": True,
            "response_temperature_property": "main.temp",
            "response_icon_property": "weather[0].icon",
            "response_wind_speed_property": "wind.speed",
            "response_wind_direction_property": "wind.deg",
            "response_humidity_property": "main.humidity",
        },
    }
