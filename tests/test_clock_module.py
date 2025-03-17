import pytest
from freezegun import freeze_time
from unittest.mock import MagicMock, patch, call
from datetime import datetime
from flem.modules.clock_module import ClockModule
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
def clock_module(mock_clock_config):
    """Fixture to create a ClockModule instance."""
    return ClockModule(config=mock_clock_config, width=9, height=11)


def test_clock_module_initialization(mock_clock_config):
    """Test the initialization of ClockModule."""
    module = ClockModule(config=mock_clock_config, width=9, height=11)

    assert module.module_name == "TestClock"
    assert module._ClockModule__config == mock_clock_config


def test_clock_module_initialization_with_invalid_config():
    """Test ClockModule initialization with an invalid config."""
    invalid_config = MagicMock()
    with patch("flem.models.modules.clock_config.ClockConfigSchema.load") as mock_load:
        mock_load.return_value = MagicMock()
        module = ClockModule(config=invalid_config, width=9, height=11)

        mock_load.assert_called_once()
        assert module._ClockModule__config is not None


def test_clock_module_start(clock_module):
    """Test the start method of ClockModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch.object(clock_module, "reset") as mock_reset,
        patch.object(clock_module, "write") as mock_write,
    ):
        clock_module.start(update_device, write_queue)

        assert clock_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_clock_module_stop(clock_module):
    """Test the stop method of ClockModule."""
    with patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop:
        clock_module.stop()

        assert clock_module.running is False
        mock_super_stop.assert_called_once()


def test_clock_module_write(clock_module):
    """Test the write method of ClockModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    # Mock the current time to ensure consistent results
    mock_time_proper_format = "12:34"
    mock_time = "1234"
    with (
        patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write,
        patch(
            "flem.modules.matrix_module.MatrixModule._write_object"
        ) as mock_super_write_object,
    ):
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )

        clock_module.running = True
        with freeze_time(f"2021-01-01 {mock_time_proper_format}", tz_offset=0):
            clock_module.write(update_device, write_queue)

        # Verify that the binary values for each digit are written to the queue
        expected_calls = []
        start_row = clock_module._ClockModule__config.position.y
        start_col = 0
        for i, char in enumerate(mock_time):
            if i == 2:
                start_row += 6
                start_col = 2
            elif i == 3:
                start_col = 6
            expected_calls.append(call(char, write_queue, start_row, start_col))
            if i < 2:
                start_col += 4

        mock_super_write_object.assert_has_calls(expected_calls, any_order=False)

        # Verify that the parent class's write method is called
        mock_super_write.assert_called_once_with(update_device, write_queue, True, None)


def test_clock_module_write_with_seconds_indicator(clock_module):
    """Test the write method with seconds indicator enabled."""
    update_device = MagicMock()
    write_queue = MagicMock()

    # Mock the current time to ensure consistent results
    mock_time_proper_format = "12:34:56"
    with (
        patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write,
        patch(
            "flem.modules.matrix_module.MatrixModule._write_object"
        ) as mock_super_write_object,
        patch(
            "flem.modules.matrix_module.MatrixModule._calculate_pips_to_show"
        ) as mock_calculate_pips,
    ):
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )
        mock_calculate_pips.return_value = 3

        clock_module.running = True
        with freeze_time(f"2021-01-01 {mock_time_proper_format}", tz_offset=0):
            clock_module.write(update_device, write_queue)

        # Verify that the pips are written to the queue
        expected_pip_calls = [
            call((8, clock_module._ClockModule__config.position.y, True)),
            call((8, clock_module._ClockModule__config.position.y + 1, True)),
            call((8, clock_module._ClockModule__config.position.y + 2, True)),
        ]
        write_queue.assert_has_calls(expected_pip_calls, any_order=False)

        # Verify that the parent class's write method is called
        mock_super_write.assert_called_once_with(update_device, write_queue, True, None)


def test_clock_module_write_handles_exceptions(clock_module):
    """Test the write method handles exceptions gracefully."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop,
        patch(
            "flem.modules.matrix_module.MatrixModule.clear_module"
        ) as mock_clear_module,
        patch("flem.modules.clock_module.logger") as mock_logger,
    ):
        clock_module.running = True

        # Simulate an exception during the write process
        write_queue.side_effect = ValueError("Test exception")
        clock_module.write(update_device, write_queue)

        # Verify that the exception is logged
        mock_logger.exception.assert_called_once_with(
            f"Error while running {clock_module.module_name}: Test exception"
        )

        # Verify that the module is stopped and cleared
        mock_super_stop.assert_called_once()
        mock_clear_module.assert_called_once_with(update_device, write_queue)
