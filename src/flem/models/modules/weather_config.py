# pylint: disable=missing-module-docstring, missing-class-docstring, unused-argument

from marshmallow import Schema, fields, post_load

from flem.models.config import ModuleConfig, ModulePositionConfig
from flem.models.config_schema import ModulePositionSchema, ModuleSchema


class WeatherConfigArguments:
    def __init__(
        self,
        api_url: str = None,
        api_key: str = None,
        city_id: int = None,
        temperature_unit: str = None,
        show_wind_speed: bool = False,
        show_humidity: bool = False,
        response_temperature_property: str = None,
        response_icon_property: str = None,
        response_wind_speed_property: str = None,
        response_wind_direction_property: str = None,
        response_humidity_property: str = None,
    ):
        self.api_url = api_url
        self.api_key = api_key
        self.city_id = city_id
        self.temperature_unit = temperature_unit
        self.response_temperature_property = response_temperature_property
        self.response_icon_property = response_icon_property
        self.show_wind_speed = show_wind_speed
        self.response_wind_speed_property = response_wind_speed_property
        self.response_wind_direction_property = response_wind_direction_property
        self.show_humidity = show_humidity
        self.response_humidity_property = response_humidity_property


class WeatherConfig(ModuleConfig):
    def __init__(
        self,
        name: str,
        module_type: str,
        position: ModulePositionConfig,
        refresh_interval: int,
        arguments: WeatherConfigArguments,
    ):
        if not arguments.temperature_unit:
            raise ValueError("Invalid temperature unit")

        super().__init__(name, module_type, position, refresh_interval, arguments)
        self.arguments = arguments


class WeatherConfigArgumentsSchema(Schema):
    api_url = fields.Str()
    api_key = fields.Str()
    city_id = fields.Int()
    temperature_unit = fields.Str()
    response_temperature_property = fields.Str()
    response_icon_property = fields.Str()
    show_wind_speed = fields.Bool()
    response_wind_speed_property = fields.Str()
    response_wind_direction_property = fields.Str()
    show_humidity = fields.Bool()
    response_humidity_property = fields.Str()

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return WeatherConfigArguments(**data)


class WeatherConfigSchema(ModuleSchema):
    name = fields.Str()
    module_type = fields.Str()
    position = fields.Nested(ModulePositionSchema)
    refresh_interval = fields.Int()
    arguments = fields.Nested(WeatherConfigArgumentsSchema)

    @post_load
    def make_module(self, data, **kwargs):
        """
        map to object
        """
        return WeatherConfig(**data)
