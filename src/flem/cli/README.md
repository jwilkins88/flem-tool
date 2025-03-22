# FLEM CLI

The FLEM CLI was birthed into this world to make managing FLEM that much easier. It's not entirely finished, but it's finished enough that it's a worthwhile addition. Several new features have been added with the advent of the CLI, including:

- **Service management**
  With the FLEM CLI, you now have the ability to run FLEM as a service. This means that it starts with your system and runs in the background. No fuss, no muss
- **Config management**
  FLEM CLI also gives you the ability to test and manage your config. More features will be added to this as time goes on, including adding modules, removing modules, adding scenes, and much, much more
- **Device management**
  The CLI also gives you a helpful way to manage your devices. With this you can change the brightness of your config without having to modify your config. You can also test your devices to ensure they're configured properly

## Setup

No setup required! It works straight out of the box. Simply run:

```
pip install flem-tool
flem device left test
```

And that's it! You're using the CLI

## Commands

The FLEM CLI has multiple commands and sub commands

```
flem --help

Usage: . [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  config   Manage the FLEM config
  device   Manage configured devices
  run      Run FLEM
  service  Manage the FLEM service
```

### Run

This starts FLEM without the service. If you're testing out a change to your config and don't want to bother with the service, then this allows you to see the logs as they happen. It's the easiest way to see if there's an error or a warning in the logs. To exit FLEM, press `ctrl+c`

`flem run`

```
flem run --help

Usage: . run [OPTIONS]

  Run FLEM

Options:
  -d, --debug         Enable debug logging.
  -l, --log-dump      Enable logging to file.
  -p, --print-matrix  Print the matrix to the console.
  --profile           Start up in profiling mode (dev only)
  --help              Show this message and exit.
```

### Config

The config command allows you to manage and validate your config. For now, it's mostly validation, but more features will come in the future

```
flem config

Usage: . config [OPTIONS] COMMAND [ARGS]...

  Manage the FLEM config

Options:
  --help  Show this message and exit.

Commands:
  edit      Opens flem config in default editor
  validate  Validate the flem config
  which     Returns the location of your current config
```

#### Edit

Opens the config file for editing in your default editor

`flem config edit`

```
Usage: . config edit [OPTIONS]

  Opens flem config in default editor

Options:
  --help  Show this message and exit.
```

#### Validate

Validate parses your current config and checks for common errors. In order it:

1. Parses the config and makes sure the entire config is syntactically correct
2. Checks the device configuration and runs a test of the devices (optional)
3. Checks the modules configured to make sure that they're valid modules. This actually loads the module to verify that it is found
4. Checks the scene configuration
   1. Checks to ensure that the modules listed in the scene exist in the configured device modules
   2. Tests the boundaries of the configured modules for the scene to ensure that:
      1. No modules overlap
      2. No modules are rendered off the screen
5. Prints the validation status

`flem config validate`

```
Usage: . config validate [OPTIONS]

  Validate the flem config

Options:
  -d, --skip-device  Skip the device validation
  -v, --verbose      Verbose output
  --help             Show this message and exit.
```

#### Which

Returns the location of the loaded config

`flem config which`

```
Usage: . config which [OPTIONS]

  Returns the location of your current config

Options:
  --help  Show this message and exit.
```

### Device

Allows you to perform operations on the devices in the config. This command expects a device for most of the operations (this is the device name from the config)

Most commands will look like `flem device left test`. If you're not sure what the names of the device are, run `flem device ls` to get a list of the devices

```
flem device

Usage: . device [OPTIONS] [DEVICE_NAME] COMMAND [ARGS]...

  Manage configured devices

Options:
  --help  Show this message and exit.

Commands:
  brightness  Sets the brightness of the device
  clear       Clear the device of any state.
  ls          List the devices in the config
  test        Tests the device by flashing it on and then off
```

#### Brightness

Allows you to adjust the brightness of a matrix without modifying the config. Useful for on the fly adjustments if it's too bright at night or too dim during the day

`flem device left brightness 10`

```
Usage: . device [DEVICE_NAME] brightness [OPTIONS] DEVICE_BRIGHTNESS

  Sets the brightness of the device

Options:
  --help  Show this message and exit.
```

#### Clear

Sometimes, the matrix state gets stuck in the event of a crash. If you're in the middle of working on a config, and you're annoyed by stuck artifacts on the device, this allows you to clear it.

`flem device left clear`

```
Usage: . device [DEVICE_NAME] clear [OPTIONS]

  Clear the device of any state. Turns all LEDs off

Options:
  --help  Show this message and exit.
```

#### ls

Lists the configured devices and their properties

`flem device ls`

```
.venv joelwilkins@squid-tank  ~/source/flem_tool  ↱ master ±  python src/flem/. device ls --help
Usage: . device [DEVICE_NAME] ls [OPTIONS]

  List the devices in the config

Options:
  --help  Show this message and exit.
```

#### Test

Tests the device by running a small animation across it. Mostly useful for configuring devices to see if you have them reversed

`flem device left test`

```
Usage: . device [DEVICE_NAME] test [OPTIONS]

  Tests the device by flashing it on and then off

Options:
  --help  Show this message and exit.
```

### Service

Manages the FLEM service. You don't need to use the service, but it is the most convenient way to run FLEM. It allows you to have FLEM start automatically with your system. It also doesn't use a terminal as it spits out logs.

```
Usage: . service [OPTIONS] COMMAND [ARGS]...

  Manage the FLEM service

Options:
  --help  Show this message and exit.

Commands:
  install    Install the FLEM service
  restart    Restart the FLEM service
  start      Start the FLEM service
  stop       Stop the FLEM service
  uninstall  Uninstall the FLEM service
```

#### Install

Installs the service and returns the status. This should only need to be done once unless you uninstall the service

`flem service install`

```
Usage: . service install [OPTIONS]

  Install the FLEM service

Options:
  --help  Show this message and exit.
```

#### Uninstall

Uninstalls the service. Really only useful if you don't want to use flem anymore or just don't want it to start with the system

`flem service uninstall`

```
Usage: . service uninstall [OPTIONS]

  Uninstall the FLEM service

Options:
  --help  Show this message and exit.
```

#### Start

Starts the service. This typically isn't required unless the service crashes or you've just installed the service.

`flem service start`

```
Usage: . service start [OPTIONS]

  Start the FLEM service

Options:
  --help  Show this message and exit.
```

#### Stop

Stops the service if it's running. If you want to save a bit of extra battery, or want to turn FLEM off during a meeting or something, this is what you'd use

`flem service stop`

```
Usage: . service stop [OPTIONS]

  Stop the FLEM service

Options:
  --help  Show this message and exit.
```

#### Restart

Combines the functionality of `flem service stop` and `flem service start`. This should only be necessary if something changes that requires more than a code change (say, updating FLEM to the latest version)

`flem service restart`

```
Usage: . service restart [OPTIONS]

  Restart the FLEM service

Options:
  --help  Show this message and exit.
```