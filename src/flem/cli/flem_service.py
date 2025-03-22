import os
import subprocess
import click


@click.group()
def service():
    """
    Manage the FLEM service
    """


@service.command()
def install():
    """
    Install the FLEM service
    """
    click.echo("Installing FLEM service")
    subprocess.call(
        [
            "sh",
            f"{os.path.dirname(os.path.abspath(__file__))}/../scripts/install_flem_service.sh",
        ]
    )
    click.echo("FLEM service installed")
    subprocess.call(["systemctl", "--user", "status", "flem.service", "--no-pager"])


@service.command()
def uninstall():
    """
    Uninstall the FLEM service
    """
    if os.path.exists(f"{os.path.expanduser('~')}/.config/systemd/user/flem.service"):
        subprocess.call(
            [
                "sh",
                (
                    f"{os.path.dirname(os.path.abspath(__file__))}"
                    "/../scripts/uninstall_flem_service.sh"
                ),
            ]
        )
        click.echo("FLEM service uninstalled")
    else:
        click.echo(click.style("Warning: FLEM service not installed", fg="yellow"))
        click.echo("Run 'flem service install' to install the FLEM service")


@service.command()
def start():
    """
    Start the FLEM service
    """
    if os.path.exists(f"{os.path.expanduser('~')}/.config/systemd/user/flem.service"):
        subprocess.call(["systemctl", "--user", "start", "flem.service"])
        click.echo("FLEM service started")
        subprocess.call(["systemctl", "--user", "status", "flem.service", "--no-pager"])
    else:
        click.echo(click.style("Warning: FLEM service not installed", fg="yellow"))
        click.echo("Run 'flem service install' to install the FLEM service")


@service.command()
def stop():
    """
    Stop the FLEM service
    """
    if os.path.exists(f"{os.path.expanduser('~')}/.config/systemd/user/flem.service"):
        subprocess.call(["systemctl", "--user", "stop", "flem.service"])
        click.echo("FLEM service stopped")
        subprocess.call(["systemctl", "--user", "status", "flem.service", "--no-pager"])
    else:
        click.echo(click.style("Warning: FLEM service not installed", fg="yellow"))
        click.echo("Run 'flem service install' to install the FLEM service")


@service.command()
def restart():
    """
    Restart the FLEM service
    """
    if os.path.exists(f"{os.path.expanduser('~')}/.config/systemd/user/flem.service"):
        subprocess.call(["systemctl", "--user", "restart", "flem.service"])
        click.echo("FLEM service restarted")
        subprocess.call(["systemctl", "--user", "status", "flem.service", "--no-pager"])
    else:
        click.echo(click.style("Warning: FLEM service not installed", fg="yellow"))
        click.echo("Run 'flem service install' to install the FLEM service")
