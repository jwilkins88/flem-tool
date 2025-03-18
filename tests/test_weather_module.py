import json
import pytest
from unittest.mock import MagicMock, patch, call
from flem.modules.weather_module import WeatherModule
from flem.models.modules.weather_config import WeatherConfig, WeatherConfigArguments
from flem.models.config import ModulePositionConfig
from flem.modules.matrix_module import MatrixModule


def stop_module(module: MatrixModule):
    """Helper function to stop the module's loop."""
    module.running = False


@pytest.fixture
def mock_weather_config():
    """Fixture to create a mock WeatherConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = WeatherConfigArguments(
        api_url="https://api.openweathermap.org/data/2.5/weather?appid={api_key}&id={city_id}&units={temperature_unit}",
        api_key="test_api_key",
        city_id=12345,
        temperature_unit="metric",
        show_humidity=True,
        show_wind_speed=True,
        response_temperature_property="main.temp",
        response_humidity_property="main.humidity",
        response_wind_speed_property="wind.speed",
        response_wind_direction_property="wind.deg",
        response_icon_property="weather.0.icon",
    )
    return WeatherConfig(
        name="TestWeather",
        module_type="Weather",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )


@pytest.fixture
def weather_module(mock_weather_config):
    """Fixture to create a WeatherModule instance."""
    with patch("flem.modules.weather_module.Timer"):
        return WeatherModule(config=mock_weather_config, width=9, height=13)


def test_weather_module_initialization(mock_weather_config):
    """Test the initialization of WeatherModule."""
    with patch("flem.modules.weather_module.Timer"):
        module = WeatherModule(config=mock_weather_config, width=9, height=13)

    assert module.module_name == "TestWeather"
    assert module._WeatherModule__config == mock_weather_config


def test_weather_module_start(weather_module):
    """Test the start method of WeatherModule."""
    update_device = MagicMock()
    write_queue = MagicMock()
    write_queue.put = MagicMock()  # Simulate the behavior of a queue's put method
    write_queue.get = MagicMock(
        return_value=None
    )  # Simulate the behavior of a queue's get method

    with (
        patch.object(weather_module, "reset") as mock_reset,
        patch.object(weather_module, "write") as mock_write,
    ):
        weather_module.start(update_device, write_queue)

        assert weather_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_weather_module_stop(weather_module):
    """Test the stop method of WeatherModule."""
    with patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop:
        weather_module.stop()

        assert weather_module.running is False
        mock_super_stop.assert_called_once()


def test_weather_module_get_weather_from_api(weather_module):
    """Test the __get_weather_from_api method."""
    with (
        patch("requests.get") as mock_requests,
        patch("builtins.open", MagicMock()) as mock_open,
    ):
        mock_requests.return_value.text = (
            '{"weather": [{"icon": "01d"}], "main": {"temp": 25.5}}'
        )

        weather_module._WeatherModule__get_weather_from_api()

        mock_requests.assert_called_once_with(
            "https://api.openweathermap.org/data/2.5/weather?appid=test_api_key&id=12345&units=metric",
            timeout=5,
        )
        mock_open.assert_called_once_with(
            weather_module._WeatherModule__weather_file, "w", encoding="utf-8"
        )
