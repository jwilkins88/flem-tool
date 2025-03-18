import pytest
from unittest.mock import MagicMock, patch, call
from flem.modules.cpu_module import CpuModule
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
def cpu_module(mock_cpu_config):
    """Fixture to create a CpuModule instance."""
    return CpuModule(config=mock_cpu_config, width=3, height=18)


def test_cpu_module_initialization(mock_cpu_config):
    """Test the initialization of CpuModule."""
    module = CpuModule(config=mock_cpu_config, width=3, height=18)

    assert module.module_name == "TestCPU"
    assert module._CpuModule__config == mock_cpu_config
    assert isinstance(module._CpuModule__line_module, MatrixModule)


def test_cpu_module_initialization_with_invalid_config():
    """Test CpuModule initialization with an invalid config."""
    invalid_config = MagicMock()
    with patch("flem.models.modules.cpu_config.CpuConfigSchema.load") as mock_load:
        mock_load.return_value = MagicMock()
        module = CpuModule(config=invalid_config, width=3, height=18)

        mock_load.assert_called_once()
        assert module._CpuModule__config is not None


def test_cpu_module_start(cpu_module):
    """Test the start method of CpuModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch.object(cpu_module, "reset") as mock_reset,
        patch.object(cpu_module, "write") as mock_write,
    ):
        cpu_module.start(update_device, write_queue)

        assert cpu_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_cpu_module_stop(cpu_module):
    """Test the stop method of CpuModule."""
    with patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop:
        cpu_module.stop()

        assert cpu_module.running is False
        mock_super_stop.assert_called_once()


def test_cpu_module_reset(cpu_module):
    """Test the reset method of CpuModule."""
    with patch("flem.modules.matrix_module.MatrixModule.reset") as mock_super_reset:
        cpu_module.reset()

        assert cpu_module._CpuModule__previous_value == "NA"
        mock_super_reset.assert_called_once()


def test_cpu_module_write(cpu_module):
    """Test the write method of CpuModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch("psutil.cpu_percent", return_value=50.0) as mock_cpu_percent,
        patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write,
        patch.object(cpu_module._CpuModule__line_module, "write") as mock_line_write,
        patch.object(cpu_module, "_write_object") as mock_write_object,
    ):
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )

        cpu_module.running = True
        cpu_module.write(update_device, write_queue)

        # Verify that the CPU usage is written to the display using _write_object
        expected_calls = [
            call(
                "c",
                write_queue,
                cpu_module._CpuModule__config.position.y,
                cpu_module._CpuModule__config.position.x,
            ),
            call(
                "5",
                write_queue,
                cpu_module._CpuModule__config.position.y + 7,
                cpu_module._CpuModule__config.position.x,
            ),
            call(
                "0",
                write_queue,
                cpu_module._CpuModule__config.position.y + 13,
                cpu_module._CpuModule__config.position.x,
            ),
        ]

        mock_write_object.assert_has_calls(expected_calls, any_order=False)

        # Verify that the line module's write method is called
        mock_line_write.assert_called_once_with(update_device, write_queue, False)

        # Verify that the parent class's write method is called
        mock_super_write.assert_called_once_with(
            update_device, write_queue, True, None, True
        )


def test_cpu_module_write_handles_exceptions(cpu_module):
    """Test the write method handles exceptions gracefully."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop,
        patch(
            "flem.modules.matrix_module.MatrixModule.clear_module"
        ) as mock_clear_module,
        patch("flem.modules.cpu_module.logger") as mock_logger,
    ):
        cpu_module.running = True

        # Simulate an exception during the write process
        write_queue.side_effect = ValueError("Test exception")
        cpu_module.write(update_device, write_queue)

        # Verify that the exception is logged
        mock_logger.exception.assert_called_once_with(
            f"Error while running {cpu_module.module_name}: Test exception"
        )

        # Verify that the module is stopped and cleared
        mock_super_stop.assert_called_once()
        mock_clear_module.assert_called_once_with(update_device, write_queue)
