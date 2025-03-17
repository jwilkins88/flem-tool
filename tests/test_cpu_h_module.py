import pytest
from unittest.mock import MagicMock, patch, call
from flem.modules.cpu_h_module import CpuHModule
from flem.models.modules.cpu_config import CpuConfig, CpuConfigArguments
from flem.models.config import ModulePositionConfig
from flem.modules.matrix_module import MatrixModule


def stop_module(module: MatrixModule):
    """Helper function to stop the module's loop."""
    module.running = False


@pytest.fixture
def mock_cpu_config():
    """Fixture to create a mock CpuConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = CpuConfigArguments(
        temp_sensor="coretemp",
        temp_sensor_index=0,
        show_temp=True,
        use_bar_graph=True,
    )
    return CpuConfig(
        name="TestCPU",
        module_type="CPU",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )


@pytest.fixture
def cpu_h_module(mock_cpu_config):
    """Fixture to create a CpuHModule instance."""
    return CpuHModule(config=mock_cpu_config, width=9, height=12)


def test_cpu_h_module_initialization(mock_cpu_config):
    """Test the initialization of CpuHModule."""
    module = CpuHModule(config=mock_cpu_config, width=9, height=12)

    assert module.module_name == "TestCPU"
    assert module._CpuHModule__config == mock_cpu_config


def test_cpu_h_module_initialization_with_invalid_config():
    """Test CpuHModule initialization with an invalid config."""
    invalid_config = MagicMock()
    with patch("flem.models.modules.cpu_config.CpuConfigSchema.load") as mock_load:
        mock_load.return_value = MagicMock()
        module = CpuHModule(config=invalid_config, width=9, height=12)

        mock_load.assert_called_once()
        assert module._CpuHModule__config is not None


def test_cpu_h_module_start(cpu_h_module):
    """Test the start method of CpuHModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch.object(cpu_h_module, "reset") as mock_reset,
        patch.object(cpu_h_module, "write") as mock_write,
    ):
        cpu_h_module.start(update_device, write_queue)

        assert cpu_h_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_cpu_h_module_stop(cpu_h_module):
    """Test the stop method of CpuHModule."""
    with patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop:
        cpu_h_module.stop()

        assert cpu_h_module.running is False
        mock_super_stop.assert_called_once()


def test_cpu_h_module_write(cpu_h_module):
    """Test the write method of CpuHModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch("psutil.cpu_percent", return_value=50.0) as mock_cpu_percent,
        patch(
            "psutil.sensors_temperatures",
            return_value={"coretemp": [MagicMock(current=60.0, label="Core 0")]},
        ) as mock_sensors_temperatures,
        patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write,
    ):
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )

        cpu_h_module.running = True
        cpu_h_module.write(update_device, write_queue)

        # Verify that CPU percentage is written as pips
        num_util_pips = 9  # 50% of 18 pips
        col = 0
        for i in range(18):
            write_queue.assert_any_call(
                (col, 7 if i % 2 == 0 else 8, True if i <= num_util_pips else False)
            )
            if i % 2 != 0:
                col += 1

        # Verify that temperature is written as pips
        num_temp_pips = 11  # 60% of 18 pips - rounded
        col = 0
        for i in range(18):
            write_queue.assert_any_call(
                (col, 12 if i % 2 == 0 else 13, True if i <= num_temp_pips else False)
            )
            if i % 2 != 0:
                col += 1

        # Verify that the parent class's write method is called
        mock_super_write.assert_has_calls(
            [
                call(update_device, write_queue, False, None),
                call(update_device, write_queue, False, None),
                call(update_device, write_queue, True, None),
            ],
            any_order=False,
        )


def test_cpu_h_module_write_handles_exceptions(cpu_h_module):
    """Test the write method handles exceptions gracefully."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop,
        patch(
            "flem.modules.matrix_module.MatrixModule.clear_module"
        ) as mock_clear_module,
        patch("flem.modules.cpu_h_module.logger") as mock_logger,
    ):
        cpu_h_module.running = True

        # Simulate an exception during the write process
        write_queue.side_effect = ValueError("Test exception")
        cpu_h_module.write(update_device, write_queue)

        # Verify that the exception is logged
        mock_logger.exception.assert_called_once_with(
            f"Error while running {cpu_h_module.module_name}: Test exception"
        )

        # Verify that the module is stopped and cleared
        mock_super_stop.assert_called_once()
        mock_clear_module.assert_called_once_with(update_device, write_queue)
