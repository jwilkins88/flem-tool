from time import sleep

import click

from flem.cli.click.custom_group import CustomGroup
from flem.devices.led_device import LedDevice
from flem.models.config import Config
from flem.models.config_schema import ConfigSchema
from flem.modules.utilities.characters import lightbulb
from flem.utilities.utilities import read_config_from_file, get_config_location


@click.group(cls=CustomGroup)
@click.argument("device_name", required=False, type=click.STRING)
@click.pass_context
def device(ctx, device_name):
    """
    Manage configured devices
    """
    ctx.ensure_object(dict)
    if device_name is not None:
        ctx.obj["device_name"] = device_name

    config_location = get_config_location()
    if config_location is None:
        click.echo(click.style("Warning: No config file found. Exiting", fg="yellow"))
        return

    ctx.obj["config_location"] = config_location


@device.command()
@click.pass_context
def ls(ctx):
    """
    List the devices in the config as well as their status
    """
    click.echo(f"Checking configured devices in {ctx.obj["config_location"]}")
    config_string = read_config_from_file()
    config: Config = ConfigSchema().loads(config_string)

    for led_device in config.devices:
        configured_device = LedDevice(led_device)
        click.echo(f"Device {led_device.name}:")
        click.echo(f"  Address: {led_device.device_address}")
        click.echo(f"  Baud Rate: {led_device.speed}")
        click.echo(f"  Brightness: {led_device.brightness}")
        click.echo(f"  Connected: {configured_device.is_open()}")


@device.command()
@click.pass_context
def test(ctx):
    """
    Tests the device by flashing it on and then off
    """
    columns_on = [
        [LedDevice.ON for _ in range(LedDevice.HEIGHT)] for _ in range(LedDevice.WIDTH)
    ]

    if not ctx.obj["device_name"]:
        click.echo(click.style("Device name argument must be specified", fg="red"))
        return

    click.echo(f"Testing device: {ctx.obj['device_name']}")
    click.echo("Connecting to device")

    specified_device = load_device_from_config(ctx.obj["device_name"])

    if specified_device is None:
        return

    specified_device.connect()

    click.echo("Connected successfully")
    click.echo("Beginning test")
    for i, column in enumerate(columns_on):
        specified_device.send_col(i, column)
        specified_device.commit_cols()
        sleep(0.2)

    j = len(columns_on) - 1
    while j >= 0:
        specified_device.send_col(j, columns_on[j])
        specified_device.commit_cols()
        j -= 1
        sleep(0.2)

    click.echo("Test successful")

    ctx.invoke(clear)
    specified_device.sleep()


@device.command()
@click.pass_context
@click.argument("device_brightness", type=click.INT)
def brightness(ctx, device_brightness):
    """
    Sets the brightness of the device
    """
    if not ctx.obj["device_name"]:
        click.echo("Device name argument must be specified")
        return

    if device_brightness < 1 or device_brightness > 255:
        click.echo(
            click.style("Warning: Brightness must be between 1 and 255", fg="yellow")
        )
        click.echo("Setting brightness to 50")
        device_brightness = 55

    specified_device = load_device_from_config(ctx.obj["device_name"])

    if specified_device is None:
        return

    click.echo(f"Connecting to device {ctx.obj["device_name"]}")
    specified_device.connect()

    click.echo(f"Setting brightness to {device_brightness}")
    specified_device.brightness(device_brightness)

    grid = [
        [LedDevice.OFF for _ in range(LedDevice.HEIGHT)] for _ in range(LedDevice.WIDTH)
    ]

    for i in range(LedDevice.WIDTH):
        if i < 1 or i > 7:
            continue
        for j in range(LedDevice.HEIGHT):
            if j < 3 or j > 12:
                continue

            grid[i][j] = lightbulb[j - 3][i - 1]

    specified_device.render_matrix(grid)

    sleep(3)

    specified_device.render_matrix(
        [
            [LedDevice.OFF for _ in range(LedDevice.HEIGHT)]
            for _ in range(LedDevice.WIDTH)
        ]
    )

    specified_device.sleep()


@device.command()
@click.pass_context
def clear(ctx):
    """
    Clear the device of any state. Turns all LEDs off
    """
    clear_all = False
    columns_off = [
        [LedDevice.OFF for _ in range(LedDevice.HEIGHT)] for _ in range(LedDevice.WIDTH)
    ]
    click.echo(ctx.obj)
    if not ctx.obj["device_name"]:
        click.echo(
            click.style("No device name specified. Clearing all devices", fg="yellow")
        )
        clear_all = True

    click.echo("Loading devices from config")
    config: Config = ConfigSchema().loads(read_config_from_file())

    for config_device in config.devices:
        if not clear_all and not config_device.name == ctx.obj["device_name"]:
            continue

        click.echo(f"Clearing device {config_device.name}")

        led_device = LedDevice(config_device)

        led_device.render_matrix(columns_off)
        led_device.sleep()


def load_device_from_config(device_name: str) -> LedDevice:
    config_string = read_config_from_file()
    config: Config = ConfigSchema().loads(config_string)

    specified_device: LedDevice = None
    for led_device in config.devices:
        if led_device.name == device_name:
            specified_device = LedDevice(led_device)
            break

    if specified_device is None:
        click.echo(click.style("Warning: Couldn't find requested device", fg="yellow"))

    return specified_device
