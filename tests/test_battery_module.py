import pytest
from unittest.mock import MagicMock, patch, call
from threading import Thread
from flem.modules.animator_module import AnimatorModule
from flem.modules.battery_module import BatteryModule
from flem.models.modules.battery_config import BatteryConfig, BatteryConfigArguments
from flem.models.config import ModulePositionConfig


def stop_module(module):
    """Helper function to stop the module's loop."""
    module.running = False


@pytest.fixture
def mock_battery_config():
    """Fixture to create a mock BatteryConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = BatteryConfigArguments(show_percentage=True, critical_threshold=20)
    return BatteryConfig(
        name="TestBattery",
        module_type="Battery",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )


@pytest.fixture
def battery_module(mock_battery_config):
    """Fixture to create a BatteryModule instance."""
    return BatteryModule(config=mock_battery_config, width=9, height=11)


def test_battery_module_initialization(mock_battery_config):
    """Test the initialization of BatteryModule."""
    module = BatteryModule(config=mock_battery_config, width=9, height=11)

    assert module.module_name == "TestBattery"
    assert module._BatteryModule__config == mock_battery_config
    assert isinstance(module._BatteryModule__charging_animation, AnimatorModule)


def test_battery_module_start(battery_module):
    """Test the start method of BatteryModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch.object(battery_module, "reset") as mock_reset,
        patch.object(battery_module, "write") as mock_write,
    ):
        battery_module.start(update_device, write_queue)

        assert battery_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_battery_module_stop(battery_module):
    """Test the stop method of BatteryModule."""
    animator_module = MagicMock()
    animator_module.stop = MagicMock()
    animator_module.running = True
    battery_module._BatteryModule__charging_animation = animator_module
    battery_module.stop()

    assert battery_module.running is False
    animator_module.stop.assert_called_once()


def test_battery_module_write(battery_module):
    """Test the write method of BatteryModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    mock_battery_info = MagicMock()
    mock_battery_info.percent = 50
    mock_battery_info.power_plugged = False

    with (
        patch("psutil.sensors_battery", return_value=mock_battery_info),
        patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write,
        patch.object(battery_module, "_write_object") as mock_write_object,
    ):
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )

        battery_module.running = True
        battery_module.write(update_device, write_queue)

        mock_write_object.assert_any_call("battery", write_queue, 0, 0)

        # Verify that the battery pips are written
        expected_pip_calls = []
        start_col = 1
        for i in range(14):
            pip_on = i < 7  # 50% of 14 pips
            if i % 2 == 0:
                expected_pip_calls.append(call((start_col, 1, pip_on)))
            else:
                expected_pip_calls.append(call((start_col, 2, pip_on)))
                start_col += 1
        write_queue.assert_has_calls(expected_pip_calls, any_order=False)

        # Verify that the percentage is written
        expected_percentage_calls = [
            call("5", write_queue, 5, 1),
            call("0", write_queue, 5, 5),
        ]
        mock_write_object.assert_has_calls(expected_percentage_calls, any_order=True)

        # Verify that the parent class's write method is called
        mock_super_write.assert_called_once_with(
            update_device, write_queue, True, None, True
        )


def test_battery_module_write_charging(battery_module):
    """Test the write method when the battery is charging."""
    update_device = MagicMock()
    write_queue = MagicMock()

    mock_battery_info = MagicMock()
    mock_battery_info.percent = 80
    mock_battery_info.power_plugged = True

    with (
        patch("psutil.sensors_battery", return_value=mock_battery_info),
        patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write,
        patch.object(
            battery_module._BatteryModule__charging_animation, "start"
        ) as mock_animation_start,
    ):
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )

        battery_module.running = True
        battery_module.write(update_device, write_queue)

        # Verify that the charging animation is started
        mock_animation_start.assert_called_once_with(update_device, write_queue, True)

        # Verify that the parent class's write method is called
        mock_super_write.assert_called_once_with(
            update_device, write_queue, True, None, True
        )


def test_battery_module_write_handles_exceptions(battery_module):
    """Test the write method handles exceptions gracefully."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop,
        patch(
            "flem.modules.matrix_module.MatrixModule.clear_module"
        ) as mock_clear_module,
        patch("flem.modules.battery_module.logger") as mock_logger,
    ):
        battery_module.running = True

        # Simulate an exception during the write process
        write_queue.side_effect = ValueError("Test exception")
        battery_module.write(update_device, write_queue)

        # Verify that the exception is logged
        mock_logger.exception.assert_called_once_with(
            f"Error while running {battery_module.module_name}: Test exception"
        )

        # Verify that the module is stopped and cleared
        mock_super_stop.assert_called_once()
        mock_clear_module.assert_called_once_with(update_device, write_queue)
