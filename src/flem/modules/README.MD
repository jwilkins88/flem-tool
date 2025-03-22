# Modules

## CPU Module

My first creation! This module simply displays the current CPU usage. As of this writing, I'm using [psutil](https://github.com/giampaolo/psutil)

**Module Type**: CpuModule

**Dimensions (width x height)**: 3x18

**Custom Arguments**: N/A

**Sample Module Config**

```json
{
  "module_type": "CpuModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000
}
```

Example:

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

## Horizontal CPU Module

Reading top to bottom is hard for those of us who are used to reading left to right. I initially created the CPU module thinking about how I could display the most information in the smallest space, but, variety is the spice of life. For when maximalism is the order of the day, consider the horizontal CPU module. It's capable of displaying both the utilization and temperature, and it's a bit easier on the eyes.

Top number shows utilization. Bottom shows temperature (celsius only for now)

This, once again, utilizes [psutil](https://github.com/giampaolo/psutil). This time, I'm using a function that only works on linux ([per the documentation](https://psutil.readthedocs.io/en/latest/#sensors)). If you're on Windows, well, I don't know that any of this will work for you.

**Module Type**: CpuHModule

**Dimensions (width x height)**: 9x12 (without temperature); 9x19 (with temperature)

**Custom Arguments**:

| Argument     | Type                                                            | Description                                                                                                                                                                      |
| :----------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `show_temp`      | true                                                         | Whether we're going to show the temperature or not. If this is set to true, `temp_sensor` and `temp_sensor_index` are required |
| `temp_sensor` | string | **If `show_temp` is true, this is required**. There's a few ways you can find your sensor name. One of the easiest is to install lm-sensors and find you sensor in the list. It's not always obvious. For my AMD processor it's `k10temp`                                                       |
| `temp_sensor_index` | int | **If `show_temp` is true, this is required** For my AMD processor, I have one sensor. When you have more than one sensor, you'll need to specify which one you want to see. Most the time, this is individual core temperature |
| `use_bar_graph` | bool | Show the CPU utilization (and, optionally, temp) as a bar graph. Slightly more compact. It uses a 2x9 grid that lights up sequentially. For both temp and utilization, I'm setting a max of 100. For now, that's hardcoded as it seems reasonable. I may make that value adjustable in case you're targeting specific temps and want to keep track of a specific threshold.<br><br>It looks pretty cool. Thanks to [Kitsunebi](https://community.frame.work/u/kitsunebi/summary) from the Framework community for the idea! |

**Sample Module Config**

```json
{
    "module_type": "CpuHModule",
    "position": {
        "x": 0,
        "y": 14
    },
    "refresh_interval": 1000,
    "arguments": {
        "show_temp": true,
        "temp_sensor": "k10temp",
        "temp_sensor_index": 0,
        "use_bar_graph": true
    }
}
```

**"use_bar_graph": false**
```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

**"use_bar_graph": true**
```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

## GPU Module

This command is a little bit more complex because it relies on an OS utility to get the GPU utilization. This is currently only tested on Linux Mint (should work fine on Ubuntu as well). I haven't tested this on Windows or any other Linux flavor. The theory is that it should work. The tool that I'm using to get the GPU info is called [NVTOP](https://github.com/Syllo/nvtop). It's a super neat utility that works with both AMD and NVIDIA (and a whole lot of other stuff). Can't say enough good things about it.

To make things even more complicated, this uses a custom version that I modified to suit my needs. I have a [PR open to get those changes into the main version](https://github.com/Syllo/nvtop/pull/358), but until that's merged and published, you're going to need to build your own version of this utility from [my fork](https://github.com/jwilkins88/nvtop/tree/master). The build instructions are really good, and I promise it's not too hard.

**Module Type**: GpuModule

**Dimensions (width x height)**: 3x18

**Custom Arguments**:

| Argument                   | Type                           | Description                                                                                                                                                                                                                                                                                                                                                      |
| :------------------------- | :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gpu_index`                | integer                        | In the case that you have multiple GPUs (iGPU and discrete GPU), you need to select your index. `0` Is a pretty safe bet for most use cases, but check the output of your command of choice (no reason this _has_ to be nvtop)                                                                                                                                   |
| `gpu_command`              | string                         | This is the command to run to get the GPU info. In my case, this is `/home/xxxxxx/nvtop-dev/usr/local/bin/nvtop`. Again, this can be whatever you want it to be so long as it outputs json                                                                                                                                                                       |
| `gpu_command_arguments`    | array[string] | If you need to specify arguments for your command, this is how you'll need to do it                                                                                                                        |
| `gpu_util_output_property` | string                         | This is the property that we're going to read from the JSON. Keep in mind that, as of now, I don't have any validation around this. I'll add that as a part of [improving error handling](#improved-error-handling), but, for now, this is fairly brittle. It can only handle digits, and I don't do any sanitization. My value for this is typically `gpu_util` |

**Sample Module Config**

```json
{
  "module_type": "GpuModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "gpu_index": 0,
    "gpu_command": "/home/xxxxxx/nvtop-dev/usr/local/bin/nvtop",
    "gpu_command_arguments": "-s",
    "gpu_util_output_property": "gpu_util"
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

## Horizontal GPU Module

Just like the [Horizontal CPU Module](#horizontal-cpu-module), this module can show temp and utilization in a left-to-right fashion. Other than that, it's exactly the same as the [GPU module](#gpu-module). All the same things apply. It's still using my custom version of [NVTOP](https://github.com/Syllo/nvtop), and you'll need that if you want to use it. The nice thing about NVTOP is that it gives me all the information I want in one go, so I don't need to worry about making multiple calls to get the utilization and then the temperature. 

**Module Type**: GpuHModule

**Dimensions (width x height)**: 9x12 (without temperature); 9x19 (with temperature)

**Custom Arguments**:

| Argument                   | Type                           | Description                                                                                                                                                                                                                                                                                                                                                      |
| :------------------------- | :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gpu_index`                | integer                        | In the case that you have multiple GPUs (iGPU and discrete GPU), you need to select your index. `0` Is a pretty safe bet for most use cases, but check the output of your command of choice (no reason this _has_ to be nvtop)                                                                                                                                   |
| `gpu_command`              | string                         | This is the command to run to get the GPU info. In my case, this is `/home/xxxxxx/nvtop-dev/usr/local/bin/nvtop`. Again, this can be whatever you want it to be so long as it outputs json                                                                                                                                                                       |
| `gpu_command_arguments`    | array[string] | If you need to specify arguments for your command, this is how you'll need to do it                                                                                                               |
| `gpu_util_output_property` | string                         | This is the property that we're going to read from the JSON. Keep in mind that, as of now, I don't have any validation around this. I'll add that as a part of [improving error handling](#improved-error-handling), but, for now, this is fairly brittle. It can only handle digits, and I don't do any sanitization. My value for this is typically `gpu_util` |
| `show_temp` | bool | Unlike the cpu temp module, this one doesn't require any extra config. Set this to true, and you can see your GPU temperature live. It's handy dandy |
| `use_bar_graph` | bool | Show the GPU utilization (and, optionally, temp) as a bar graph. Slightly more compact. It uses a 2x9 grid that lights up sequentially. For both temp and utilization, I'm setting a max of 100. For now, that's hardcoded as it seems reasonable. I may make that value adjustable in case you're targeting specific temps and want to keep track of a specific threshold.<br><br>It looks pretty cool. Thanks to [Kitsunebi](https://community.frame.work/u/kitsunebi/summary) from the Framework community for the idea! |

**Sample Module Config**

```json
{
  "module_type": "GpuModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "gpu_index": 1,
    "gpu_command": "/home/xxxxxx/nvtop-dev/usr/local/bin/nvtop",
    "gpu_command_arguments": "-s",
    "gpu_util_output_property": "gpu_util",
    "show_temp": true
  }
}
```

**"use_bar_graph": false**
```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

**"use_bar_graph": true**
```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

## Line Module

This is most useful as a "sub-module". I use it in both the [CPU Module](#cpu-module) and the [GPU Module](#gpu-module), but it also has more uses. Currently, this is my only "static" module (i.e., it doesn't run a thread, and it never updates - unless there's a config update). Currently only supports horizontal lines.

**Module Type**: LineModule

**Dimensions (width x height)**: \[width\]x1

**Custom Arguments**:

| Argument     | Type                                                            | Description                                                                                                                                                                      |
| :----------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `width`      | integer                                                         | Specifies how many pixels the line will span. I have no validation around this, but I will plan on adding some as a part of [improving error handling](#improved-error-handling) |
| `line_style` | string<br>Allowed values: `solid`, `dashed`<br>Default: `solid` | Specifies whether the line is solid or separate by one pixel set to off. Very naive implementation and needs to be improved                                                      |

**Sample Module Config**

```json
{
  "module_type": "LineModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "line_style": "dashed",
    "width": 9
  }
},
{
  "module_type": "LineModule",
  "position": {
    "x": 0,
    "y": 2
  },
  "refresh_interval": 1000,
  "arguments": {
    "line_style": "solid",
    "width": 9
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛  DASHED
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛  SOLID
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

## Clock Module

This is a simple clock module that shows the current system time. Why use a module when you have a clock on your computer? Because it's dope. There's no other reason you need. Optionally, displays an indicator showing the progression of seconds until the next minute (think of it like a seconds hand, but with far less precision). The seconds indicator blinks, giving another indicator of seconds passing. One full cycle of blinks (blink on, blink off) represents 2 seconds. I might add support for custom timezones.

**Module Type**: ClockModule

**Dimensions (width x height)**: 9x11

**Custom Arguments**:

| Argument                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `clock_mode`             | string<br>Allowed values: `12h`, `24h`<br>Default: `12h` | Specifies whether you want to show 12 hour time, or 24 hour time (i.e., 03:30 vs 15:30)                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `show_seconds_indicator` | boolean                                                  | Display the seconds indicator. This is a little bit complicated, but I realized that, with the style I have for the clock, I'd always have 10 pixels to spare (5 to the right of the hours, 5 to the left of the minutes). In order to capitalize on that space, I came up with a way to show the progression through the minute, but at a lower precision than we're typically used to. This also blinks. I might add an option to disable the blink if people think it's annoying, but I think it's cool |

**Sample Module Config**

```json
{
  "module_type": "ClockModule",
  "position": {
    "x": 0,
    "y": 1
  },
  "refresh_interval": 1000,
  "arguments": {
    "clock_mode": "24h",
    "show_seconds_indicator": true
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚪ ⚪ ⚫ ⚫ ⚪ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

## Binary Clock Module

Another cool idea from [Kitsunebi](https://community.frame.work/u/kitsunebi/summary). Based off the KDE Plasma binary clock, this tracks time using the magic of binary! For users who are comfortable reading binary, this module saves a lot of precious real estate. It also just looks super cool. It's really lively with the seconds column constantly changing, so it'a a really neat module to have on your display. The one thing that doesn't work great is that it's 6 pixels wide, and our display is 9 pixels wide. That means that it can't be centered. Not a big deal, though, and maybe I'll come up with some sort of a companion for it to fill in the 3 pixel gap. I'll think on it.

In a binary clock, each row represents a bit (on/off). In order to read the column value, you transpose the digits into a standard binary string. From my example below:

```
8️⃣⚪
4️⃣⚫
2️⃣⚫
1️⃣⚫
```

Would be transposed as:

```
⚪⚫⚫⚫ = 1000
```

Which equals 8. If we do that for the rest of the grid below,

```
8️⃣⚫ ⚪ ⚫ ⚫ ⚫ ⚪
4️⃣⚫ ⚫ ⚫ ⚪ ⚫ ⚫
2️⃣⚫ ⚫ ⚫ ⚪ ⚫ ⚫
1️⃣⚪ ⚪ ⚪ ⚫ ⚪ ⚫
```

We get `19:16:18` as the current time

Pretty cool stuff. Try it out!

**Module Type**: BinaryClockModule

**Dimensions (width x height)**: 6x4

**Custom Arguments**:

| Argument                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `clock_mode`             | string<br>Allowed values: `12h`, `24h`<br>Default: `12h` | Specifies whether you want to show 12 hour time, or 24 hour time (i.e., 03:30 vs 15:30)                                                                                                                                                                                                                                                                                                                                                                                                                    |
```json
{
  "name": "binary_clock",
  "module_type": "BinaryClockModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "clock_mode": "24h"
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

## RAM Module

Shows current RAM usage. Once again, this uses psutil. Should work on Windows, but I'm not going to be testing on Windows for a little while. This currently only shows RAM usage rounded to the nearest gigabyte. I did add an indicator (similar to the [clock module](#clock-module)) that shows little pips for each 1/9th of a gigabyte. In the sample output below, I'm using ~9.1GB of RAM.

**Module Type**: RamModule

**Dimensions (width x height)**: 9x11

**Custom Arguments**: N/A

**Sample Module Config**

```json
{
  "name": "ram",
  "module_type": "RamModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

## Animator Module

This one is big. I can see this being the bread and butter of most setups. Allows arbitrary "animations" through config. It can also display static drawings if you only have one frame and set the frame duration to 0. The frame duration overrides the module level `refresh_interval`. For this specific type of module, the refresh interval is irrelevant, but for now it'll need to be set to some arbitrary value. I'll fix that in the future

See examples animations that I've made (poorly) in the [weather animation directory](src/flem/animator_files/)

**Module Type**: AnimatorModule

**Dimensions (width x height)**: *no set size. specify in config*

**Custom Arguments**:

| Argument                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frames`             | array[Frame]  | This is what sets all the individual frames for the module. I'll define the frames object below |
| `width` | int | Necessary to let the module know how many columns it will span |
| `height` | int | Necessary to let the module know how many rows it will span |
| `animation_file` | string | This can be a path to anywhere on your system, but it has to be an absolute path (for now). I.E., `/home/blah/.flem/animator_files/my_animation/animation.json`. I recommend sticking this in flem's home directory just so they're all in the same place. I provide this because animations can get lengthy and bloat your config. See examples in the [animator_files directory](src/flem/animator_files/) |

<br>

**Frame Object**

| Property                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frame` | array[array[int]] | This defines a single frame for the animation. If there's only one animation, it'll just be a static drawing
| `frame_duration` | int | This is how long the frame should display (in milliseconds). If this is set to 0, it is considered a static frame, and no frame changes will happen. |

**Full Module Config**

```json
{
  "name": "animator",
  "module_type": "AnimatorModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "frames": [
      {
          "frame": [
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 1, 1, 0 ,0],
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]
          ],
          "frame_duration": 1000
      },
      {
          "frame": [
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 1 ,0],
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 1, 1, 1, 1, 1, 0, 0],
              [0, 1, 0, 1, 0, 1, 0, 1, 0]
          ],
          "frame_duration": 1000
      }
    ],
    "width": 9,
    "height": 6
  }
}
```

**File Module Config**

```json
{
  "name": "animator",
  "module_type": "AnimatorModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "animation_file": "/home/myuser/.flem/animator_files/weather/fog.json",
    "width": 9,
    "height": 6
  }
}
```

```
FRAME 1

⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛

FRAME 2

⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛

```

## Weather Module

The weather module is one of the more complex modules that I've built to date. It's mostly complicated because it relies on something other than easily obtained system data. I've set it up so that it can *theoretically* use most APIs that return the weather with a simple `get` request, but I recommend setting it up with `OpenWeatherMap`, since that's what I've done my testing with. If you'd like to use a different service, reach out, and I'll see what I can do to make it happen.

In its most basic form, the weather module shows the current conditions (via an animated header) and the temperature (you choose between `imperial`, `standard`, or `metric`). It has an option to show the humidity as well as an option to show wind speed and direction.

This is a **BIG** module. Big as in, it'll take up a lot of the panel. I highly recommend swapping this one in via scenes or not enabling all the stats and just using the temperature if you're concerned about real estate.

Because this makes an external API call, I wanted to keep performance in mind and I'm using a cached file in the `~/.flem` directory. The module will make one API call every 10 minutes to update the cache file, and the module will load the results from that file when it refreshes. I'm considering making an option to have that update parameterized, but, for now, it's set statically at 10 minutes.

I'll make some instructions for how to set up your API key in a future update, but it's a pretty straight forward process. In brief:

1. Head to https://openweathermap.org/
2. Sign up for an account
3. Go to your user profile and find `My API Keys`
4. Generate a new key
5. Stick it in the config
6. Find your city id by searching for your city and copying it from the URL
   1. example: `https://openweathermap.org/city/4997787` - Copy 4997787

For the URL string, it's important that you note that there are some key placeholders that have to be there (especially if you're trying some service other than `openweathermap`). Those are:

1. `{city_id}` - This is just a string, so if your service goes by string rather than an integer id, that should be fine
2. `{api_key}` - This is obviously your api key. Very important
3. `{temperature_unit}` - This is probably the most optional, but for now it's still required or my code will break

If you want to use this and make it as simple as possible, copy the example config below and pop your API key in. It'll work right out of the box.


**Module Type**: WeatherModule

**Dimensions (width x height)**: 

* Just temperature
  * 9x14
* With Humidity or Wind Speed
  * 9x22
* With all
  * 9x30

**Custom Arguments**:

| Argument                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api_url`             | string  | The API endpoint to make the request to. For now, I recommend sticking with what I know will work, and that value is: `"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&cnt=5&units={temperature_unit}"` |
| `api_key` | string | This is the api key that you'll create for your service. Absolutely required |
| `city_id` | string | For openweathermap, this is an integer, but I'm using a string to make this as compatible as possible with other services that folks may want to use |
| `response_temperature_property` | string | This is a json selector. If you're using `openweathermap`, this will be `main.temp`. If you're using anything else, you'll have to inspect the response object and set accordingly |
| `response_icon_property` | string | This is a json selector. If you're using `openweathermap`, this will be `weather.[0].main`. If you're using anything else, you'll have to inspect the response object and set accordingly. This is the current condition. I support all of the statuses [specified by OpenWeatherMap](https://openweathermap.org/weather-conditions). I don't support the sub-conditions right now, just the main groups |
| `show_wind_speed` | bool | Whether or not to show the wind speed information along with the weather. If this is specified, **you must** also specify `response_wind_direction_property` and `response_wind_speed_property` |
| `response_wind_speed_property` | string | This is a json selector. If you're using `openweathermap`, the value will be `wind.speed`. If you're using anything else, you'll have to inspect the json response and adjust accordingly |
| `response_wind_direction_property` | string | This is a json selector. If you're using `openweathermap`, the value will be `wind.deg`. If you're using anything else, you'll have to inspect the json response and adjust accordingly. <br>**NOTE**: The module code is expecting this to be in degrees (i.e., 0 degrees == North). If your API returns cardinal directions, **it will not work** |
| `show_humidity`| bool | Shows the humidity in percent. If this is set to `true`, **you must** also specify `response_humidity_property`
| `response_humidity_property` | string | This is a json selector. If you're using `openweathermap`, this will be `main.humidity`. If you're using anything else, you'll have to inspect the json response and adjust accordingly.

**Sample Module Config**

```json
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
    "api_key": "<my api key>",
    "city_id": "4997787",
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
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛  ANIMATED CONDITION INDICATOR
⬛ ⚫ ⚫ ⚪ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚪ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚪ ⚪ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚪ ⬛  TEMPERATURE
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛  HUMIDITY
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⬛  WIND SPEED
⬛ ⚪ ⚫ ⚪ ⚪ ⚫ ⚪ ⚫ ⚫ ⚫ ⬛
⬛ ⚪ ⚫ ⚪ ⚪ ⚪ ⚪ ⚫ ⚪ ⚫ ⬛  WIND DIRECTION INDICATOR (showing southwest here) 
⬛ ⚪ ⚫ ⚪ ⚫ ⚫ ⚪ ⚪ ⚫ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```

## Battery Module

The battery module is a compact display that can show just the battery icon or, optionally, the numeric percentage. This module uses `psutil` to retrieve the battery information. The battery module has a few different states:

**Unplugged**

In this state, the current percentage "pip" blinks on and off to indicate a discharge state

**Plugged in**

In this state, an animation shows the battery filling from the current percentage "pip" to full. It follows the same sequence as all the other bars that I've implemented with pips. After the full battery animation finished, it resets to the current charge for 2 seconds

**Critical**

This is set to show when the battery reaches a minimum (configurable) threshold. In this state, all the battery pips will blink

| Argument                 | Type                                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `show_percentage`             | bool  | Whether or not the numeric percentage shows below the battery icon |
| `critical_threshold` | int | The battery percentage where the pips start blinking to indicate it's time to charge your laptop |


**Battery Module Config**

```json
{
  "name": "battery",
  "module_type": "BatteryModule",
  "position": {
    "x": 0,
    "y": 0
  },
  "refresh_interval": 1000,
  "arguments": {
    "show_percentage": true,
    "critical_threshold": 20
  }
}
```

```
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚫ ⚫ ⚫ ⚫ ⚪ ⬛
⬛ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚫ ⚫ ⚪ ⚫ ⚪ ⚫ ⚪ ⚫ ⬛
⬛ ⚫ ⚪ ⚪ ⚪ ⚫ ⚪ ⚪ ⚪ ⚫ ⬛
⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
```