import os
import subprocess
import click
from loguru import logger

from flem.cli.flem_device import test
from flem.models.config import Config
from flem.models.config_schema import ConfigSchema
from flem.utilities.utilities import (
    get_config_location,
    load_module,
    read_config_from_file,
)


@click.group()
def config():
    """
    Manage the FLEM config
    """
    config_location = get_config_location()
    if config_location is None:
        click.echo("Warning: No config file found. Exiting")
        return


@config.command()
def which():
    click.echo(get_config_location())


@config.command()
@click.pass_context
def validate(ctx):
    """
    Validate the flem config
    """
    click.echo("Validating config")

    config_string = read_config_from_file()
    loaded_config: Config = ConfigSchema().loads(config_string)

    click.echo("Config loaded successfully")

    click.echo("Validating devices")

    ctx.ensure_object(dict)

    for config_device in loaded_config.devices:
        click.echo()
        click.echo("===================")
        click.echo()
        ctx.obj["device_name"] = config_device.name
        ctx.invoke(test)

    click.echo()
    click.echo("Device tests successful. Testing modules")
    click.echo()
    for config_device in loaded_config.devices:
        click.echo(
            f"Detected {len(config_device.modules)} moduele{"s" if len(config_device.modules) > 1 else ""} for device {config_device.name}"
        )
        click.echo()
        click.echo(f"Validating modules")
        click.echo()
        module_positions: list[dict] = []
        for module in config_device.modules:
            click.echo("===================")
            click.echo()
            click.echo(f"Validating module {module.module_type}:{module.name}")
            click.echo()
            click.echo("Module Config:")
            click.echo("    Position:")
            click.echo(f"        x: {module.position.x}")
            click.echo(f"        y: {module.position.y}")
            click.echo(f"   Refresh Interval: {module.refresh_interval}")
            if len(module.arguments) > 0:
                click.echo(f"   Arguments:")
                for key, value in module.arguments.items():
                    click.echo(f"       {key}: {value}")
            click.echo()
            click.echo("Attempting to load module")
            loaded_module = load_module(module)
            click.echo("Successfully loaded module")
            click.echo()

        print(module_positions)


@config.command()
def uninstall():
    """
    Uninstall the FLEM service
    """
    if os.path.exists(f"{os.path.expanduser('~')}/.config/systemd/user/flem.service"):
        subprocess.call(["sh", "./uninstall_flem_service.sh"])
        logger.info("FLEM service uninstalled")
    else:
        logger.warning("FLEM service not installed")


@config.command()
def start():
    """
    Start the FLEM service
    """
    if os.path.exists(f"{os.path.expanduser('~')}/.config/systemd/user/flem.service"):
        subprocess.call(["systemctl", "--user", "start", "flem.service"])
        logger.info("FLEM service started")
    else:
        logger.warning("FLEM service not installed")
        logger.info("Run 'flem service install' to install the FLEM service")


@config.command()
def stop():
    """
    Stop the FLEM service
    """
    if os.path.exists(f"{os.path.expanduser('~')}/.config/systemd/user/flem.service"):
        subprocess.call(["systemctl", "--user", "stop", "flem.service"])
        logger.info("FLEM service stopped")
    else:
        logger.warning("FLEM service not installed")
        logger.info("Run 'flem service install' to install the FLEM service")


@config.command()
def restart():
    """
    Restart the FLEM service
    """
    if os.path.exists(f"{os.path.expanduser('~')}/.config/systemd/user/flem.service"):
        subprocess.call(["systemctl", "--user", "restart", "flem.service"])
        logger.info("FLEM service restarted")
    else:
        logger.warning("FLEM service not installed")
        logger.info("Run 'flem service install' to install the FLEM service")
