import pytest
from freezegun import freeze_time
from unittest.mock import MagicMock, patch, call
from datetime import datetime
from flem.modules.binary_clock_module import BinaryClockModule
from flem.models.modules.clock_config import ClockConfig, ClockConfigArguments
from flem.models.config import ModulePositionConfig
from flem.modules.matrix_module import MatrixModule


def stop_module(module: MatrixModule):
    """Helper function to stop the module's loop."""
    module.running = False


@pytest.fixture
def mock_clock_config():
    """Fixture to create a mock ClockConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = ClockConfigArguments(clock_mode="12h", show_seconds_indicator=True)
    return ClockConfig(
        name="TestClock",
        module_type="Clock",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )


@pytest.fixture
def binary_clock_module(mock_clock_config):
    """Fixture to create a BinaryClockModule instance."""
    return BinaryClockModule(config=mock_clock_config, width=6, height=4)


def test_binary_clock_module_initialization(mock_clock_config):
    """Test the initialization of BinaryClockModule."""
    module = BinaryClockModule(config=mock_clock_config, width=6, height=4)

    assert module.module_name == "TestClock"
    assert module._BinaryClockModule__config == mock_clock_config


def test_binary_clock_module_initialization_with_invalid_config():
    """Test BinaryClockModule initialization with an invalid config."""
    invalid_config = MagicMock()
    with patch("flem.models.modules.clock_config.ClockConfigSchema.load") as mock_load:
        mock_load.return_value = MagicMock()
        module = BinaryClockModule(config=invalid_config, width=6, height=4)

        mock_load.assert_called_once()
        assert module._BinaryClockModule__config is not None


def test_binary_clock_module_start(binary_clock_module):
    """Test the start method of BinaryClockModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch.object(binary_clock_module, "reset") as mock_reset,
        patch.object(binary_clock_module, "write") as mock_write,
    ):
        binary_clock_module.start(update_device, write_queue)

        assert binary_clock_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_binary_clock_module_stop(binary_clock_module):
    """Test the stop method of BinaryClockModule."""
    with patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop:
        binary_clock_module.stop()

        assert binary_clock_module.running is False
        mock_super_stop.assert_called_once()


def test_binary_clock_module_write(binary_clock_module):
    """Test the write method of BinaryClockModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    # Mock the current time to ensure consistent results
    mock_time_proper_format = "12:34:56"
    mock_time = "123456"
    with (
        patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write,
        patch(
            "flem.modules.matrix_module.MatrixModule._write_array"
        ) as mock_super_write_array,
    ):
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )

        binary_clock_module.running = True
        with freeze_time(f"2021-01-01 {mock_time_proper_format}", tz_offset=0):
            binary_clock_module.write(update_device, write_queue)

        # Verify that the binary values for each digit are written to the queue
        expected_calls = []
        for i, char in enumerate(mock_time):
            expected_calls.append(
                call(
                    binary_clock_module._BinaryClockModule__binary_values[char],
                    binary_clock_module._BinaryClockModule__config.position.y,
                    binary_clock_module._BinaryClockModule__config.position.x + i,
                    write_queue,
                )
            )

        mock_super_write_array.assert_has_calls(expected_calls, any_order=False)

        # Verify that the parent class's write method is called
        mock_super_write.assert_called_once_with(
            update_device, write_queue, True, None, True
        )


def test_binary_clock_module_write_handles_exceptions(binary_clock_module):
    """Test the write method handles exceptions gracefully."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop,
        patch(
            "flem.modules.matrix_module.MatrixModule.clear_module"
        ) as mock_clear_module,
        patch("flem.modules.binary_clock_module.logger") as mock_logger,
    ):
        binary_clock_module.running = True

        # Simulate an exception during the write process
        write_queue.side_effect = ValueError("Test exception")
        binary_clock_module.write(update_device, write_queue)

        # Verify that the exception is logged
        mock_logger.exception.assert_called_once_with(
            f"Error while running {binary_clock_module.module_name}: Test exception"
        )

        # Verify that the module is stopped and cleared
        mock_super_stop.assert_called_once()
        mock_clear_module.assert_called_once_with(update_device, write_queue)
