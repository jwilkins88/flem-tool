import pytest
from unittest.mock import MagicMock, patch, call
from flem.modules.gpu_h_module import GpuHModule
from flem.models.modules.gpu_config import GpuConfig, GpuConfigArguments
from flem.models.config import ModulePositionConfig
from flem.modules.matrix_module import MatrixModule


def stop_module(module: MatrixModule):
    """Helper function to stop the module's loop."""
    module.running = False


@pytest.fixture
def mock_gpu_config():
    """Fixture to create a mock GpuConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = GpuConfigArguments(
        gpu_command="nvidia-smi",
        gpu_command_arguments=[
            "--query-gpu=utilization.gpu,temperature.gpu",
            "--format=json",
        ],
        gpu_index=0,
        gpu_temp_property="temp",
        gpu_util_property="gpu_util",
        show_temp=True,
        use_bar_graph=True,
    )
    return GpuConfig(
        name="TestGPU",
        module_type="GPU",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )


@pytest.fixture
def gpu_h_module(mock_gpu_config):
    """Fixture to create a GpuHModule instance."""
    return GpuHModule(config=mock_gpu_config, width=9, height=12)


def test_gpu_h_module_initialization(mock_gpu_config):
    """Test the initialization of GpuHModule."""
    module = GpuHModule(config=mock_gpu_config, width=9, height=12)

    assert module.module_name == "TestGPU"
    assert module._GpuHModule__config == mock_gpu_config
    assert isinstance(module._GpuHModule__line_module, MatrixModule)
    assert isinstance(module._GpuHModule__temperature_line_module, MatrixModule)


def test_gpu_h_module_initialization_with_invalid_config():
    """Test GpuHModule initialization with an invalid config."""
    invalid_config = MagicMock()
    with patch("flem.models.modules.gpu_config.GpuConfigSchema.load") as mock_load:
        mock_load.return_value = MagicMock()
        module = GpuHModule(config=invalid_config, width=9, height=12)

        mock_load.assert_called_once()
        assert module._GpuHModule__config is not None


def test_gpu_h_module_start(gpu_h_module):
    """Test the start method of GpuHModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch.object(gpu_h_module, "reset") as mock_reset,
        patch.object(gpu_h_module, "write") as mock_write,
    ):
        gpu_h_module.start(update_device, write_queue)

        assert gpu_h_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_gpu_h_module_stop(gpu_h_module):
    """Test the stop method of GpuHModule."""
    with patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop:
        gpu_h_module.stop()

        assert gpu_h_module.running is False
        mock_super_stop.assert_called_once()


def test_gpu_h_module_reset(gpu_h_module):
    """Test the reset method of GpuHModule."""
    with patch("flem.modules.matrix_module.MatrixModule.reset") as mock_super_reset:
        gpu_h_module.reset()

        assert gpu_h_module._GpuHModule__previous_value == "NA"
        assert gpu_h_module._GpuHModule__previous_temp == "NA"
        mock_super_reset.assert_called_once()


def test_gpu_h_module_write(gpu_h_module):
    """Test the write method of GpuHModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    mock_gpu_info = {
        0: {
            "utilization.gpu": "50%",
            "temperature.gpu": "60C",
        }
    }

    with (
        patch(
            "subprocess.check_output",
            return_value='[{"device_name":"AMD Radeon RX 7700S","gpu_clock":"255MHz","mem_clock":"96MHz","temp":"60C","fan_speed":"29%","power_draw":"1W","gpu_util":"50%","mem_util":"0%"},{"device_name":"AMD Radeon 780M Graphics","gpu_clock":"800MHz","mem_clock":"2800MHz","temp":"45C","fan_speed":"CPU Fan","power_draw":"11W","gpu_util":"12%","mem_util":"39%"}]',
        ) as mock_subprocess,
        patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write,
        patch.object(gpu_h_module._GpuHModule__line_module, "write") as mock_line_write,
        patch.object(
            gpu_h_module._GpuHModule__temperature_line_module, "write"
        ) as mock_temp_line_write,
    ):
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )

        gpu_h_module.running = True
        gpu_h_module.write(update_device, write_queue)

        # Verify that GPU usage and temperature are written
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

        # Verify that the line modules' write methods are called
        mock_line_write.assert_called_once_with(update_device, write_queue, False)
        mock_temp_line_write.assert_called_once_with(update_device, write_queue, False)

        # Verify that the parent class's write method is called
        mock_super_write.assert_called_once_with(update_device, write_queue, True, None)


def test_gpu_h_module_write_handles_exceptions(gpu_h_module):
    """Test the write method handles exceptions gracefully."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop,
        patch(
            "flem.modules.matrix_module.MatrixModule.clear_module"
        ) as mock_clear_module,
        patch("flem.modules.gpu_h_module.logger") as mock_logger,
    ):
        gpu_h_module.running = True

        # Simulate an exception during the write process
        write_queue.side_effect = ValueError("Test exception")
        gpu_h_module.write(update_device, write_queue)

        # Verify that the exception is logged
        mock_logger.exception.assert_called_once_with(
            f"Error while running {gpu_h_module.module_name}: Test exception"
        )

        # Verify that the module is stopped and cleared
        mock_super_stop.assert_called_once()
        mock_clear_module.assert_called_once_with(update_device, write_queue)
