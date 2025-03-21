import os
import subprocess
import click
from loguru import logger

from flem.cli.flem_device import test
from flem.models.config import Config, DeviceConfig, SceneConfig, ModuleConfig
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
@click.option(
    "--skip-device",
    "-d",
    default=False,
    help="Skip the device validation",
    is_flag=True,
)
@click.option(
    "--verbose",
    "-v",
    default=False,
    help="Verbose output",
    is_flag=True,
)
@click.pass_context
def validate(ctx, skip_device, verbose):
    """
    Validate the flem config
    """
    click.echo("Validating config")
    click.echo()

    config_string = read_config_from_file()
    loaded_config: Config = ConfigSchema().loads(config_string)

    click.echo("Config loaded successfully")
    click.echo()

    ctx.ensure_object(dict)

    if skip_device:
        click.echo("Skipping device validation")
    else:
        click.echo("Validating devices")
        for config_device in loaded_config.devices:
            click.echo()
            click.echo("===================")
            click.echo()
            ctx.obj["device_name"] = config_device.name
            ctx.invoke(test)
            click.echo("Device test successful")

    click.echo()
    click.echo("Testing modules")
    click.echo()
    module_positions: list[dict] = []
    errors: list[dict] = []
    for config_device in loaded_config.devices:
        click.echo(
            f"Detected {len(config_device.modules)} moduele{"s" if len(config_device.modules) > 1 else ""} for device {config_device.name}"
        )
        click.echo()
        click.echo(f"Validating modules")
        for module in config_device.modules:
            click.echo()
            click.echo(f"Validating module {module.module_type}:{module.name}")
            if verbose:
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

            module_positions.append(
                {
                    "device": config_device.name,
                    "module_name": module.name,
                    "module_type": module.module_type,
                    "grid_coords": {
                        "grid_start": {
                            "x": module.position.x,
                            "y": module.position.y,
                        },
                        "grid_end": {
                            "x": module.position.x + loaded_module.width - 1,
                            "y": module.position.y + loaded_module.height - 1,
                        },
                    },
                }
            )

        click.echo()

    click.echo("Validating scenes")
    click.echo()
    for device in loaded_config.devices:
        for scene in device.scenes:
            click.echo(f"Validating scene {scene.name} for device {device.name}")
            click.echo()
            if verbose:
                click.echo("Scene Config:")
                click.echo(f"   Name: {scene.name}")
                click.echo(f"   Show For: {scene.show_for}")
                click.echo(f"   Scene Order: {scene.scene_order}")
                click.echo("   Modules:")
                for module in scene.modules:
                    click.echo(f"       - {module}")
                click.echo()

            click.echo("Validating module positions")
            click.echo()

            scene_modules: list[str] = []

            for module in scene.modules:
                scene_module = next(
                    (
                        item
                        for item in module_positions
                        if item["device"] == device.name
                        and item["module_name"] == module
                    ),
                    None,
                )
                if scene_module is None:
                    errors.append(
                        {
                            "device_name": device.name,
                            "scene_name": scene.name,
                            "module_name": module["module_name"],
                            "error_text": f"Error: Module {module} not found in device {device.name}",
                            "error_type": "scene",
                        }
                    )
                else:
                    scene_modules.append(scene_module)

            for module in scene_modules:
                for neighbor in scene_modules:
                    if module == neighbor:
                        continue

                    if (
                        module["grid_coords"]["grid_start"]["x"]
                        <= neighbor["grid_coords"]["grid_end"]["x"]
                        and module["grid_coords"]["grid_end"]["x"]
                        >= neighbor["grid_coords"]["grid_start"]["x"]
                        and module["grid_coords"]["grid_start"]["y"]
                        <= neighbor["grid_coords"]["grid_end"]["y"]
                        and module["grid_coords"]["grid_end"]["y"]
                        >= neighbor["grid_coords"]["grid_start"]["y"]
                    ):
                        errors.append(
                            {
                                "device_name": device.name,
                                "scene_name": scene.name,
                                "module_name": module["module_name"],
                                "error_text": f"Error: {module['module_name']} overlaps {neighbor['module_name']}",
                                "error_type": "module",
                            }
                        )

                if module["grid_coords"]["grid_start"]["x"] < 0:
                    errors.append(
                        {
                            "device_name": device.name,
                            "scene_name": scene.name,
                            "module_name": module["module_name"],
                            "error_text": f"Error: Module {module['module_name']} starts outside the grid",
                            "error_type": "module",
                        }
                    )
                if module["grid_coords"]["grid_start"]["y"] < 0:
                    errors.append(
                        {
                            "device_name": device.name,
                            "scene_name": scene.name,
                            "module_name": module["module_name"],
                            "error_text": f"Error: Module {module['module_name']} starts outside the grid",
                            "error_type": "module",
                        }
                    )
                if module["grid_coords"]["grid_end"]["x"] > 8:
                    errors.append(
                        {
                            "device_name": device.name,
                            "scene_name": scene.name,
                            "module_name": module["module_name"],
                            "error_text": f"Error: Module {module['module_name']} ends outside the grid",
                            "error_type": "module",
                        }
                    )
                if module["grid_coords"]["grid_end"]["y"] > 33:
                    errors.append(
                        {
                            "device_name": device.name,
                            "scene_name": scene.name,
                            "module_name": module["module_name"],
                            "error_text": f"Error: Module {module['module_name']} ends outside the grid",
                            "error_type": "module",
                        }
                    )
            click.echo()

    if len(errors) > 0:
        click.echo(click.style("Errors found:", fg="red"))
        click.echo()
        for error in errors:
            click.echo(click.style(f"Device: {error['device_name']}", fg="red"))
            click.echo(click.style(f"   Scene: {error['scene_name']}", fg="red"))
            click.echo(click.style(f"       Module: {error['module_name']}", fg="red"))
            click.echo(
                click.style(f"           Error: {error['error_text']}", fg="red")
            )
    else:
        click.echo("No errors found")
        click.echo("Config validated successfully")


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
