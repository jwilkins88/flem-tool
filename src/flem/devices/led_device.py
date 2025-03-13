# pylint: disable=missing-module-docstring

from enum import IntEnum
import serial

from loguru import logger

from flem.models.config import DeviceConfig


class CommandVals(IntEnum):
    """
    CommandVals is an enumeration of command values used for controlling a matrix display.

    Attributes:
        Brightness (int): Command to set the brightness level (0x00).
        Pattern (int): Command to set the display pattern (0x01).
        BootloaderReset (int): Command to reset the bootloader (0x02).
        Sleep (int): Command to put the display to sleep (0x03).
        Animate (int): Command to start an animation (0x04).
        Panic (int): Command to trigger a panic mode (0x05).
        Draw (int): Command to draw on the display (0x06).
        StageGreyCol (int): Command to stage a grey column (0x07).
        DrawGreyColBuffer (int): Command to draw from the grey column buffer (0x08).
        SetText (int): Command to set text on the display (0x09).
        StartGame (int): Command to start a game (0x10).
        GameControl (int): Command to control game actions (0x11).
        GameStatus (int): Command to get the game status (0x12).
        SetColor (int): Command to set the color (0x13).
        DisplayOn (int): Command to turn the display on (0x14).
        InvertScreen (int): Command to invert the screen colors (0x15).
        SetPixelColumn (int): Command to set a pixel column (0x16).
        FlushFramebuffer (int): Command to flush the framebuffer (0x17).
        ClearRam (int): Command to clear the RAM (0x18).
        ScreenSaver (int): Command to activate the screensaver (0x19).
        SetFps (int): Command to set the frames per second (0x1A).
        SetPowerMode (int): Command to set the power mode (0x1B).
        PwmFreq (int): Command to set the PWM frequency (0x1E).
        DebugMode (int): Command to activate debug mode (0x1F).
        Version (int): Command to get the version information (0x20).
    """

    BRIGHTNESS = 0x00
    PATTERN = 0x01
    BOOT_LOADER_RESET = 0x02
    SLEEP = 0x03
    ANIMATE = 0x04
    PANIC = 0x05
    DRAW = 0x06
    STAGE_GREY_COL = 0x07
    DRAW_GREY_COLUMN_BUFFER = 0x08
    SETTEXT = 0x09
    START_GAME = 0x10
    GAME_CONTROL = 0x11
    GAME_STATUS = 0x12
    SET_COLOR = 0x13
    DISPLAY_ON = 0x14
    INVERT_SCREEN = 0x15
    SET_PIXEL_COLUMN = 0x16
    FLUSH_FRAME_BUFFER = 0x17
    CLEAR_RAM = 0x18
    SCREENSAVER = 0x19
    SET_FPS = 0x1A
    SET_POWER_MODE = 0x1B
    PWM_FREQ = 0x1E
    DEBUG_MODE = 0x1F
    VERSION = 0x20


class LedDevice:
    __serial_device = None
    __response_size = 32
    __fwk_magic = [0x32, 0xAC]

    WIDTH: int = 9
    HEIGHT: int = 34
    ON: int = 0xFF
    OFF: int = 0x00
    name: str = None

    def __init__(self, config: DeviceConfig):
        self.__config = config
        self.name = self.__config.name

    def connect(self) -> None:
        """
        Establishes a serial connection to the device.

        This method initializes a serial connection using the specified
        location and speed attributes of the device.

        Raises:
            serial.SerialException: If the connection to the serial device fails.
        """
        self.__serial_device = serial.Serial(
            self.__config.location, self.__config.speed
        )

        self.brightness(self.__config.brightness)

    def update_config(self, config: DeviceConfig) -> None:
        """
        Updates the device configuration.

        Args:
            config (DeviceConfig): The new configuration for the device.
        """
        self.close()
        self.__config = config
        self.connect()

    def close(self) -> None:
        """
        Closes the serial connection to the device.

        This method closes the serial connection to the device if it is open.
        """
        if self.__serial_device is not None and self.__serial_device.is_open:
            self.__serial_device.close()

    def is_open(self) -> bool:
        """
        Check if the serial device is open.

        Returns:
            bool: True if the serial device is open, False otherwise.
        """
        if not self.__serial_device:
            return False

        return self.__serial_device.is_open

    def send_serial(self, command: CommandVals) -> None:
        """Send serial command by using existing serial connection"""
        try:
            self.__serial_device.write(command)
        except (IOError, OSError) as _ex:
            logger.exception(f"Error: {_ex}")

    def send_command(
        self, command: CommandVals, parameters: list = None, with_response: bool = False
    ) -> bytes:
        """
        Sends a command to the specified device.

        Args:
            dev: The device to which the command is sent.
            command: The command to be sent.
            parameters (list, optional): A list of parameters to be sent with the command.
                Defaults to an empty list if not provided.
            with_response (bool, optional): Indicates whether a response is expected
            from the device.
                Defaults to False.

        Returns:
            The response from the device if with_response is True, otherwise None.
        """
        if parameters is None:
            parameters = []
        return self.send_command_raw(
            self.__fwk_magic + [command] + parameters,
            with_response,
        )

    def send_command_raw(
        self, command: CommandVals, with_response: bool = False
    ) -> bytes:
        """Send a command to the device.
        Opens new serial connection every time"""
        try:
            self.__serial_device.write(command)

            if with_response:
                res = self.__serial_device.read(self.__response_size)
                return res
            return None
        except (IOError, OSError) as _ex:
            logger.exception(f"Error: {_ex}")
            if self.is_open():
                self.close()
                self.connect()
            return None

    def send_col(self, x, vals: list[int]) -> None:
        """Stage greyscale values for a single column. Must be committed with commit_cols()"""
        command = self.__fwk_magic + [CommandVals.STAGE_GREY_COL, x] + vals
        self.send_serial(command)

    def commit_cols(self) -> None:
        """Commit the changes from sending individual cols with send_col(), displaying the matrix.
        This makes sure that the matrix isn't partially updated."""
        command = self.__fwk_magic + [CommandVals.DRAW_GREY_COLUMN_BUFFER, 0x00]
        self.send_serial(command)

    def render_matrix(self, matrix: list[list[int]]) -> ModuleNotFoundError:
        """Show a black/white matrix
        Send everything in a single command"""
        vals = [0x00 for _ in range(39)]

        for x in range(9):
            for y in range(34):
                i = x + 9 * y
                if matrix[x][y]:
                    vals[int(i / 8)] = vals[int(i / 8)] | (1 << i % 8)

        self.send_command(CommandVals.DRAW, vals)

    def brightness(self, brightness: int):
        """Adjust the brightness scaling of the entire screen."""
        self.send_command(CommandVals.BRIGHTNESS, [brightness])

    def __str__(self):
        return str(
            f"Device: {self.__config.name} at {self.__config.location}",
            f"({self.__config.speed} baud)",
        )
