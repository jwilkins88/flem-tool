# FLEM Tool - Framework Light Emitting Matrix Tool
[![Pylint](https://github.com/jwilkins88/flem_tool/actions/workflows/build.yml/badge.svg)](https://github.com/jwilkins88/flem_tool/actions/workflows/build.yml)

<img src="docs/images/logo.jpeg" height="400px" />

##### Disclaimer: This is only somewhat tested, somewhat optimized, and somewhat incomplete. It works on my machine though


## What is FLEM

When I got my LED Matrices from Framework, my head was spinning with the possibilities. As I implemented things that I wanted, I realized that what I really wanted was a utility that could manage all these different pieces that I wanted in a sane way. Managing the layout of the matrices was a bit painful. Having to keep track of what LEDs were lit by what piece was painful, so I started writing a utility that would help manage that.

Enter the FLEM Tool. FLEM Tool is a config based renderer that renders modules (more on that later) for [Framework's LED Matrix panels](https://frame.work/products/16-led-matrix) asynchronously (i.e., each module updates independently). Each module manages its own space, its own content, refresh rate, etc...

I hope you find it as useful as I have!

<img src="docs/images/flem_action.jpg" height="400" />

## Table of Contents
- [Key Features](#key-features)
- [Basic Information](#basic-information)
- [Setup](#setup)
- [Customizing](#customizing)
  - [Config Reference](#config-reference)
  - [Existing Modules](#existing-modules)
  - [Adding Custom Modules (WIP)](#adding-custom-modules-wip)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Key Features

- **Modular, Asynchronous Design**  
  FLEM's architecture allows each module to update independently, ensuring smooth operation and flexible configurations.

- **Scene Management**  
  Display multiple modules in rotating scenes, maximizing the limited matrix real estate. Scenes are fully customizable and support automatic transitions.

- **Prebuilt Modules**  
  Comes with a variety of ready-to-use modules, including:
  - **CPU and GPU Usage**: Minimalist and full modules available, with optional temperature monitoring.
  - **Clock Modules**: Standard digital clock, binary clock, and more.
  - **RAM Usage**: Displays current memory usage.
  - **Weather Module**: Displays real-time weather conditions, temperature, and optional humidity/wind details.
  - **Animator Module**: Supports animated frames or static graphics for custom visuals.

- **Custom Configuration**  
  Easily customize layouts and behavior using a JSON-based config file. Add modules, adjust positions, refresh intervals, and more.

- **Open API Integration**  
  Modules like the Weather Module support external APIs for live data, with configurable endpoints and data mapping.

- **Support for Multi-Device Setup**  
  Manage multiple LED matrices with a single configuration, enabling cohesive displays across devices.

- **Lightweight and Efficient**  
  Designed to run seamlessly on Linux (tested on Linux Mint/Ubuntu), ensuring low resource usage and high performance.

- **Built for Tinkerers**  
  Encourages customization and user-driven development, with a roadmap for features like trigger configs and multi-threading.

### Scene Transition + Animator Module

![alt text](docs/images/action.gif)

## Basic Information

FLEM Tool is a way to easily manage your LED Matrix Panels from Framework. It takes a modular, asynchronous approach to updating and managing the panels. This means that you can have many modules updating on their own schedule, and you only have to worry about what's in your config file. The plan is to ship this with some prebuilt modules and give users the tools they need to build whatever they want.

As of the latest update, Scenes are supported, and this makes the tool even more useful. Scenes automatically rotate through a pre-defined list of modules at a set interval, giving users the ability to show more information on the same screen. Think of it like those obnoxious digital billboards that are everywhere now.

### Modules

Modules are the core of FLEM. Each module is self-contained, and is only concerned about rendering its own information to the matrix. Each module runs in isolation, and isn't affected by other modules that are also running (well, sort of... more on that in [limitations](#limitations)). See [the modules documentation for more details](src/flem/modules)

Currently, I have:

- CPU
  - [Minimalist CPU Module](src/flem/modules#cpu-module)
  - [Full CPU Module (includes CPU temp)](src/flem/modules#horizontal-cpu-module)
- GPU***
  - [Minimalist GPU Module](src/flem/modulesgpu-module)
  - [Full GPU Module (include GPU temp)](src/flem/modules#horizontal-gpu-module)
- Clocks
  - [Clock Module](src/flem/modulesclock-module)
  - [Binary Clock Module](src/flem/modules#binary-clock-module)
- [RAM Module](src/flem/modulesram-module)
- [Battery Module](src/flem/modules#battery-module)
- [Weather Module](src/flem/modules#weather-module)
- [Animator Module](src/flem/modules#animator-module)
- [Line Module (more of a building block)](src/flem/modules#line-module)

*** The GPU module **will not** work out of the box. It requires a custom built version of NVTOP (can be found on my github). I'm hoping that my changes will make it to the stable version of NVTOP, but, for now, there's a bit of monkeying required to get the GPU modules working. See [the GPU module](#gpu-module) section for more information

### Scenes

Scenes add power to FLEM. Scenes are exactly what they sound like. It's the ability to have a rotating selection of modules display on your matrix(s). Scenes show for a preset amount of time before loading the next set of modules and refreshing the display. Right now, the scene transition is a bit clunky and jarring, but I have plans of adding animated scene changes in the future. 

Scenes are set up independently from modules. What that means is that you define your modules (per matrix), and then scenes just reference the module configuration by name. This way, you don't have to set up the same module multiple times if its reused across scenes (i.e., always show clock module, but rotate GPU/CPU).

Scenes provides the foundation work for [trigger configs](#add-trigger-configs--in-progress). I'm excited to get to that one, but I'm working out all the basics and fundamentals before I start trying to get fancy.

## Setup

This is still a work in progress. The end goal is to have this be a package that you can install with either pip or a package manager on your favorite OS. For now, you're going to have to clone the repo and run it manually. When you clone the repository, it won't just fire up. without installing a couple dependencies.

### Before you get started

This is untested on anything except my system with my environment. Eventually, I'll add more robust testing, but I'm not going to bother with that until I feel like I'm in a pretty good place with the tool (or people start wanting to use it)

**Python versions**: 
- 3.13
- 3.12
- 3.11
- 3.10
- 3.9

If you want to check your Python version, just type `python --version` in your terminal. I have done rudimentary testing Python versions 3.9+. I haven't gotten around to doing thorough testing in anything but 3.13. Your mileage may vary

### Installing

```bash
pip install flem-tool
```

### Running Flem

FLEM comes with a default layout that's very, very basic. If you want to customize it, you'll have to create your own config. The default config is buried in the python directory, and I don't recommend messing around in there too much. See [Customizing](#customizing) for more details on how you can configure flem

```bash
flem run
```

Once that's done, your terminal should be spitting out logs, and you should see things happening on your matrix(s)!

#### Installing as a service

There's a couple benefits to installing FLEM as a service:

1. FLEM runs automatically in the background
2. FLEM runs with your computer at startup

This is a fairly hands off approach, and if you're not constantly tinkering with the config (like I am), running as a service is a great and simple way to go.

##### Install and start the service

```
flem service install
flem service start
```

For more CLI commands, see the [CLI documentation](src/flem/cli/README.md)

## Customizing

### Config Location

FLEM creates a config file at `~/.flem/config.json` on its first run. If this ever gets deleted, it'll create it again with the default config

### Config Reference

Simple Config. This is a pretty bare bones example of a config that will show the CPU module in the top left corner of the matrix. As of now, we have to add at least one scene. Scenes are what really unlock the power and flexibility of FLEM, but more on that later

```json
{
  "devices": [
    {
      "name": "left",
      "device_address": "/dev/ttyACM1",
      "speed": 115200,
      "brightness": 3,
      "on_bytes": 1,
      "off_bytes": 0,
      "modules": [
        {
          "name": "cpu",
          "module_type": "CpuHModule",
          "position": {
            "x": 0,
            "y": 0
          },
          "refresh_interval": 1000
        }
      ],
      "scenes": [
        {
          "name": "Scene 1",
          "show_for": 0,
          "scene_order": 0,
          "modules": [
            "cpu"
          ]
        }
      ]
    }
  ]
}
```

Here's the full structure of the config and all the allowed properties

```json
{
  // An array of devices
  "devices": [
    {
      //Just a string. Any value is fine here
      "name": "left",

      /**
      This value does matter. Please refer to Framework's documentation
      for what this should be.

      For Linux, this is usually "/dev/ttyACM0" or "/dev/ttyACM1"

      For Windows, ????
      **/
      "device_address": "/dev/ttyACM1",

      // This is the baud rate for the device. The default is 115200
      "speed": 115200,

      /**
      This is a value between 0 and 255. 255 is extremely bright.

      I usually run mine between 3 and 10
      **/
      "brightness": 10,

      /**
      The following two fields probably aren't necessary, but I figure
      it can't hurt.

      I'll probably make these optional at some point, and add a "device_type"
      field that will inform what these values should be
      **/
      "on_bytes": 1,
      "off_bytes": 0,

      /**
      This is an array of the modules that we want to load.
      This is where the magic happens. These modules are defined once per device
      and then referenced in the scenes. This way, we don't have to duplicate 
      modules if we have multiple scenes with the same module.
      (i.e., we want to show clock and CPU in scene 1 and Clock and GPU in Scene 2)
      **/
      "modules": [
        {
          /**
          The name is how the scenes will reference the module. This way, we can 
          have multiple of the same module, but referenced differently in scenes.
          (i.e., When I implement trigger configs, we might want to define two CPU
          Modules, but have them displayed at different coordinates)
          **/
          "name": "my_module_1",

          /**
          Module Type has a list of values. Refer to the "Existing Modules"
          section for a rundown on what their values are as well as a list
          of options for the modules.

          This will break if it doesn't match the module
          **/
          "module_type": "MyModule",

          /**
          This is an object that defines the physical location (start column, start row)
          of the module on the display. It is important to note that most of
          my stock modules have a required width and height. I suspect that most
          modules will probably have the same requirement.

          This is important to get right because it will crash the tool (for now) if
          a module gets too big for its britches
          **/
          "position": {
            // Valid values: 0-8
            "x": 0,

            // Value values: 0-33
            "y": 0
          },

          /**
          Refresh interval defines how often the module will update its value (in ms).

          I haven't done a lot of testing around how frequently these updates
          can happen before things start breaking, but just try to keep this sane

          As an example, there's not really much of a reason the clock needs to
          update more than once a second.

          When you're dealing with threading in Python, we really only have one thread,
          so, if we have 6 modules updating every 1 ms, this is probably going to
          result in havoc for everything. Feel free to experiment with this, but I
          may end up introducing a lower limit for this value as I test things

          A sane default for this is 1000
          **/
          "refresh_interval": 1000,

          /**
          This is a freeform object. As I was developing modules, I realized that we're
          going to have some modules that need a little bit more configurability than
          others. I didn't want to make specific module configs for every module, but
          I did want to provide flexibility. For the values that the individual module
          requires, see the module's documentation. The values below are just examples
          **/
          "arguments": {
            "clock_timezone": "CDT",
            "file_path": "~/my_file.txt"
            // etc...
          }
        }
      ],
      /**
      Scenes is how we can display a ton of information on a small display. Scenes are
      simply a collection of modules that rotate on an interval. I haven't tested an 
      upper limit on the number of scenes, but theoretically, you can have as many as you
      want
      **/
      "scenes": [
        {
          /**
          This doesn't have any special functionality around it. This can really be whatever
          you want, but it'll be easier to troubleshoot if all the scene names are unique. It
          could be anything: "Clock+GPU", "Clock+Weather", "Clock+CPU+GPU". This really only
          shows up in the logs
          **/
          "name": "Scene 1",

          /**
          How long this scene shows before changing (in ms). This can be different for every 
          scene or the same. It's really up to you on how you want the info to display

          NOTE: 0 means that the scene never changes
          **/
          "show_for": 20000,

          /**
          Not currently implemented, but it will be very soon. This was added as more of a 
          convenience than anything else. Rather than having to futz with reordering the json
          array, you can set the order, and it will be reflected
          **/
          "scene_order": 0,

          /**
            This array determines what modules will show in this scene.

            IMPORTANT!!! These values **MUST** match the name of a module defined in the 
            modules section above. If it doesn't, it will error
          **/
          "modules": [
            "my_module_1"
          ]
        }
      ]
    }
  ]
}
```

### Adding Custom Modules (WIP)

Currently, I don't have a way for you to do this locally, so you'll have to clone this repo and work inside of it. Eventually, I want to be able to have you plug in modules that aren't a part of this tool itself. I'd recommend starting with the line module as a template and build out from there.

There's no real gotchas at this point except that it's just a bit whacky working with a 9x34 display. Math is hard. Most my bugs have been because I suck at math.

## Limitations

This is largely untested. I've only tested it on Linux Mint. Eventually I'll get around to testing it on Windows and other distros, but for now, I can only guarantee it'll work on what's running on my laptop. Ubuntu should be fine, but if you're on any other distro, I can't guarantee anything. I'm working toward it though!

### About Modules

The dream and hope for this is that we can run completely sandboxed modules that have no impact on any other modules. This is partially true in FLEM's current state. While modules don't care about anything but doing their job, it is possible that modules can collide and render on top of each other. It's fully on the end user right now to make sure this doesn't happen. I'm planning on putting in guard rails and true sandboxing for modules in a future update, but it's just not there right now. I'm focused on core functionality (with some fun stuff), and then I'll go back and get around to hardening the application

## Roadmap

In no specific order, here's a list of things that I'm still working on getting to

#### Modify LED matrix firmware to allow for atomic "pixel" updates

Currently, the firmware only allows you to write an entire matrix at once. This works fine, but I'd prefer to have fewer shared resources between the modules. As your number of modules increases, so, too, does contention between threads for updates. The ideal end state is to have each module (and its thread) completely decoupled from the state of the matrix. As far as each module is concerned, it's living in its own sandbox

This would be a bit of an overhaul for all the existing code, and, when (if) this happens, I'll make sure I bake in backward compatibility and feature detection so this doesn't stop working if your matrix doesn't have the custom firmware. Backward compatibility is essential

I've started looking into this, and Rust bends my brain a bit. I know enough to know that it's possible, but I'm just not in a place to make this change yet. I will eventually get around to it, but it is feasible

#### Create a C# version of FLEM

This is mostly because I'm a Microsoft fan boy. I'm a .NET developer by day, and C# will always be my first love. But also:

Managing threads in Python is gross. I want true multi-threading for all sorts of reasons. The overhead will be lower in a compiled language, and I'll have a lot more flexibility in how I manage and prioritize the threads.

When (if) this happens, I will try to maintain feature parity between the two versions (python and C#). I'm also thinking about making a core functions library in C++ so that I can make most my updates in one place. I'm not a C++ developer, so that will be a long way down the road. My goal is to keep this light and fairly unopinionated, so there shouldn't be too much in the "core" functionality anyway

#### Add "trigger configs" * In Progress!

I wanted to add some clarity to this one now that I've been sitting on it for a while. I think I'm going to have different types of triggers. The obvious ones to me are:

1. APIs - Poll an API and switch scenes to show the updated information (think about a stock ticker as a poor example, or a weather warning, or a sports game score changing)
2. Event Variables - This one is probably the simplest to implement, but as an example, I use [manghud](https://github.com/flightlessmango/MangoHud) when I'm gaming, and that works off of an environment variable (`MANGOHUD=1`). Polling for that variable being set could trigger changes in scenes and show more gaming related data
3. System events - Think, updates, low battery alerts, whatever flows through the system events. Again, I'm not sure of the feasibility of this, but I can't imagine it'll be that hard

#### More modules * In Progress

I've made pretty good progress here (see [modules docs](/src/flem/modules) for details), but I've still got a couple things that I'd like to figure out:

1. RAM Bar
2. Network utilization (maybe)
3. Date module - This seems like a no brainer, but I'll probably just add this as an argument to the [clock module](/src/flem/modules#clock-module)
4. FPS module (may be difficult depending on the data availability)

#### Mega Matrix

Again, I'm bad at naming things, but I've had the idea that if I could join both my matrices (currently one on the left and one on the right) into a single screen, I'd have so much more room for activities. With the current architecture, this just isn't possible. It's something I definitely want to consider at some point though (reading text top to bottom just isn't great). This might be more of a gimmick, but it's something I want to look into

#### Bundle my version of NVTOP with FLEM

I've been thinking about the usefulness (rather, lack of) of the GPU module, and I think I need to add my compiled version of that into FLEM somehow. It's possible that I may just add is as a [cli](/src/flem/cli/README.md) to download an artifact from github and place it in the flem home directory. That'd allow folks to use the GPU modules without going through the hassle of building it themselves. I need to think about this a little bit more, but it's probably going to happen soon.

## Contributing

I'd love to see the community excited about this project and wanting to make it better. If you've got something to add (or just want to make it your own), please do! I'm open to feature requests, but even better than that, I'd love to see your ideas in the form of a PR.

I don't really have any guidelines right now, but if you want to build something on top of this, I'd love to see it. If you have a module you want to contribute, please see my [guide on making modules](#adding-custom-modules-wip).

If you make something, I'd love to give you a shout out. If you want to make your own module (but don't want to contribute it back to the tool), I'll happily add a link and a gallery showing off your awesome work.

## My current configuration

```
            LEFT                                        RIGHT
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛           ⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚫ ⚫ ⬛           ⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛           ⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛           ⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛           ⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⬛           ⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛           ⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛           ⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛           ⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛           ⬛ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛           ⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛           ⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚫ ⬛           ⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛           ⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛           ⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛           ⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛           ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

```json
{
  "devices": [
    {
      "name": "left",
      "device_address": "/dev/ttyACM1",
      "speed": 115200,
      "brightness": 100,
      "on_bytes": 1,
      "off_bytes": 0,
      "modules": [
        {
          "name": "cpu",
          "module_type": "CpuHModule",
          "position": {
            "x": 0,
            "y": 12
          },
          "refresh_interval": 1000,
          "arguments": {
            "show_temp": true,
            "temp_sensor": "k10temp",
            "temp_sensor_index": 0,
            "use_bar_graph": true
          }
        },
        {
          "name": "clock",
          "module_type": "ClockModule",
          "position": {
            "x": 0,
            "y": 0
          },
          "refresh_interval": 1000,
          "arguments": {
            "clock_mode": "24h",
            "show_seconds_indicator": true
          }
        },
        {
          "name": "weather",
          "module_type": "WeatherModule",
          "position": {
            "x": 0,
            "y": 0
          },
          "refresh_interval": 10000,
          "arguments": {
            "api_url": "https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&cnt=5&units={temperature_unit}",
            "api_key": "api_key",
            "city_id": "123467",
            "show_wind_speed": true,
            "show_humidity": true,
            "temperature_unit": "imperial",
            "response_temperature_property": "main.temp",
            "response_icon_property": "weather.0.main",
            "response_wind_speed_property": "wind.speed",
            "response_wind_direction_property": "wind.deg",
            "response_humidity_property": "main.humidity"
          }
        }
      ],
      "scenes": [
        {
          "name": "scene 1",
          "show_for": 10000,
          "scene_order": 0,
          "modules": [
            "clock",
            "cpu"
          ]
        },
        {
          "name": "scene 2",
          "show_for": 10000,
          "scene_order": 1,
          "modules": [
            "weather"
          ]
        }
      ]
    },
    {
      "name": "right",
      "device_address": "/dev/ttyACM0",
      "speed": 115200,
      "brightness": 100,
      "on_bytes": 1,
      "off_bytes": 0,
      "modules": [
        {
          "name": "battery",
          "module_type": "BatteryModule",
          "position": {
            "x": 0,
            "y": 0
          },
          "refresh_interval": 1000,
          "arguments": {
            "show_percentage": true
          }
        },
        {
          "name": "gpu_0",
          "module_type": "GpuHModule",
          "position": {
            "x": 0,
            "y": 11
          },
          "refresh_interval": 1000,
          "arguments": {
            "show_temp": true,
            "gpu_index": 0,
            "gpu_command": "/home/xxxxx/nvtop-dev/usr/local/bin/nvtop",
            "gpu_command_arguments": [
              "-s"
            ],
            "gpu_util_property": "gpu_util",
            "gpu_temp_property": "temp",
            "use_bar_graph": true
          }
        },
        {
          "name": "gpu_1",
          "module_type": "GpuHModule",
          "position": {
            "x": 0,
            "y": 11
          },
          "refresh_interval": 1000,
          "arguments": {
            "show_temp": true,
            "gpu_index": 1,
            "gpu_command": "/home/xxxxxx/nvtop-dev/usr/local/bin/nvtop",
            "gpu_command_arguments": [
              "-s"
            ],
            "gpu_util_property": "gpu_util",
            "gpu_temp_property": "temp",
            "use_bar_graph": true
          }
        },
        {
          "name": "ram",
          "module_type": "RamModule",
          "position": {
            "x": 0,
            "y": 0
          },
          "refresh_interval": 1000
        }
      ],
      "scenes": [
        {
          "name": "scene 1",
          "show_for": 10000,
          "scene_order": 0,
          "modules": [
            "gpu_0",
            "battery"
          ]
        },
        {
          "name": "scene 2",
          "show_for": 10000,
          "scene_order": 1,
          "modules": [
            "gpu_1",
            "ram"
          ]
        }
      ]
    }
  ]
}
```