import pytest
from unittest.mock import MagicMock, patch, call
from flem.devices.led_device import LedDevice, CommandVals
from flem.models.config import DeviceConfig


@pytest.fixture
def mock_device_config():
    """Fixture to create a mock DeviceConfig."""
    return DeviceConfig(
        name="TestDevice",
        device_address="/dev/ttyUSB0",
        speed=9600,
        brightness=128,
        on_bytes=1,
        off_bytes=0,
        modules=[],
        scenes=[],
    )


@pytest.fixture
def led_device(mock_device_config):
    """Fixture to create a LedDevice instance."""
    return LedDevice(config=mock_device_config)


def test_led_device_initialization(mock_device_config):
    """Test the initialization of the LedDevice class."""
    device = LedDevice(config=mock_device_config)
    assert device.name == "TestDevice"
    assert device.WIDTH == 9
    assert device.HEIGHT == 34
    assert device.ON == 0xFF
    assert device.OFF == 0x00


def test_led_device_connect(led_device):
    """Test the connect method of the LedDevice class."""
    with patch("serial.Serial") as mock_serial:
        led_device.connect()
        mock_serial.assert_called_once_with("/dev/ttyUSB0", 9600)
        led_device.brightness(128)


def test_led_device_close(led_device):
    """Test the close method of the LedDevice class."""
    led_device._LedDevice__serial_device = MagicMock(is_open=True)
    led_device.close()
    led_device._LedDevice__serial_device.close.assert_called_once()


def test_led_device_is_open(led_device):
    """Test the is_open method of the LedDevice class."""
    led_device._LedDevice__serial_device = MagicMock(is_open=True)
    assert led_device.is_open() is True

    led_device._LedDevice__serial_device.is_open = False
    assert led_device.is_open() is False

    led_device._LedDevice__serial_device = None
    assert led_device.is_open() is False


def test_led_device_send_serial(led_device):
    """Test the send_serial method of the LedDevice class."""
    led_device._LedDevice__serial_device = MagicMock()
    led_device.send_serial(CommandVals.DRAW)
    led_device._LedDevice__serial_device.write.assert_called_once_with(CommandVals.DRAW)


def test_led_device_send_command(led_device):
    """Test the send_command method of the LedDevice class."""
    with patch.object(led_device, "send_command_raw") as mock_send_command_raw:
        led_device.send_command(CommandVals.DRAW, [1, 2, 3], with_response=True)
        mock_send_command_raw.assert_called_once_with(
            [0x32, 0xAC, CommandVals.DRAW, 1, 2, 3], True
        )


def test_led_device_send_command_raw(led_device):
    """Test the send_command_raw method of the LedDevice class."""
    led_device._LedDevice__serial_device = MagicMock()
    led_device._LedDevice__serial_device.read.return_value = b"response"

    # Test with response
    response = led_device.send_command_raw([CommandVals.DRAW], with_response=True)
    led_device._LedDevice__serial_device.write.assert_called_once_with(
        [CommandVals.DRAW]
    )
    led_device._LedDevice__serial_device.read.assert_called_once_with(32)
    assert response == b"response"

    # Test without response
    led_device._LedDevice__serial_device.reset_mock()
    response = led_device.send_command_raw([CommandVals.DRAW], with_response=False)
    led_device._LedDevice__serial_device.write.assert_called_once_with(
        [CommandVals.DRAW]
    )
    assert response is None


def test_led_device_send_col(led_device):
    """Test the send_col method of the LedDevice class."""
    with patch.object(led_device, "send_serial") as mock_send_serial:
        led_device.send_col(1, [0x01, 0x02, 0x03])
        mock_send_serial.assert_called_once_with(
            [0x32, 0xAC, CommandVals.STAGE_GREY_COL, 1, 0x01, 0x02, 0x03]
        )


def test_led_device_commit_cols(led_device):
    """Test the commit_cols method of the LedDevice class."""
    with patch.object(led_device, "send_serial") as mock_send_serial:
        led_device.commit_cols()
        mock_send_serial.assert_called_once_with(
            [0x32, 0xAC, CommandVals.DRAW_GREY_COLUMN_BUFFER, 0x00]
        )


def test_led_device_render_matrix(led_device):
    """Test the render_matrix method of the LedDevice class."""
    matrix = [[1 for _ in range(34)] for _ in range(9)]
    with patch.object(led_device, "send_command") as mock_send_command:
        led_device.render_matrix(matrix)
        mock_send_command.assert_called_once()


def test_led_device_brightness(led_device):
    """Test the brightness method of the LedDevice class."""
    with patch.object(led_device, "send_command") as mock_send_command:
        led_device.brightness(200)
        mock_send_command.assert_called_once_with(CommandVals.BRIGHTNESS, [200])


def test_led_device_str(led_device):
    """Test the string representation of the LedDevice class."""
    result = str(led_device)
    assert "Device: TestDevice" in result
    assert "/dev/ttyUSB0" in result
    assert "9600 baud" in result
