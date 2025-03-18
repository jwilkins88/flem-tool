import pytest
from unittest.mock import MagicMock, patch, call
from flem.modules.ram_module import RamModule
from flem.models.config import ModuleConfig, ModulePositionConfig
from flem.modules.matrix_module import MatrixModule


def stop_module(module: MatrixModule):
    """Helper function to stop the module's loop."""
    module.running = False


@pytest.fixture
def mock_ram_config():
    """Fixture to create a mock ModuleConfig for RAM."""
    position = ModulePositionConfig(x=0, y=0)
    return ModuleConfig(
        name="TestRAM",
        module_type="RAM",
        position=position,
        refresh_interval=1000,
        arguments=None,
    )


@pytest.fixture
def ram_module(mock_ram_config):
    """Fixture to create a RamModule instance."""
    return RamModule(config=mock_ram_config, width=9, height=11)


def test_ram_module_initialization(mock_ram_config):
    """Test the initialization of RamModule."""
    module = RamModule(config=mock_ram_config, width=9, height=11)

    assert module.module_name == "TestRAM"
    assert module._RamModule__config == mock_ram_config


def test_ram_module_start(ram_module):
    """Test the start method of RamModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch.object(ram_module, "reset") as mock_reset,
        patch.object(ram_module, "write") as mock_write,
    ):
        ram_module.start(update_device, write_queue)

        assert ram_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_ram_module_stop(ram_module):
    """Test the stop method of RamModule."""
    with patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop:
        ram_module.stop()

        assert ram_module.running is False
        mock_super_stop.assert_called_once()


def test_ram_module_reset(ram_module):
    """Test the reset method of RamModule."""
    with patch("flem.modules.matrix_module.MatrixModule.reset") as mock_super_reset:
        ram_module.reset()

        assert ram_module._RamModule__previous_value == ["NA", 0]
        mock_super_reset.assert_called_once()


def test_ram_module_write(ram_module):
    """Test the write method of RamModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    # Mock memory usage
    mock_memory = MagicMock()
    mock_memory.used = 4.25 * 1000 * 1000 * 1000  # 4.25 GB
    with (
        patch("psutil.virtual_memory", return_value=mock_memory),
        patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write,
        patch.object(ram_module, "_write_object") as mock_write_object,
    ):
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )

        ram_module.running = True
        ram_module.write(update_device, write_queue)

        # Verify that the whole number is written with a leading zero
        expected_calls = [
            call("0", write_queue, ram_module._RamModule__config.position.y, 0),
            call("4", write_queue, ram_module._RamModule__config.position.y, 4),
        ]
        mock_write_object.assert_has_calls(expected_calls, any_order=False)

        # Verify that the fraction is written as pips (rounded to 1/9th)
        expected_pip_calls = []
        for i in range(9):
            pip_col = 8 if i <= 4 else 0
            pip_row = ram_module._RamModule__config.position.y + i + (1 if i > 4 else 0)
            expected_pip_calls.append(call((pip_col, pip_row, i < 2)))  # 2/9th of 100
        write_queue.assert_has_calls(expected_pip_calls, any_order=False)

        # Verify that the parent class's write method is called
        mock_super_write.assert_called_once_with(
            update_device, write_queue, True, None, True
        )


def test_ram_module_write_handles_exceptions(ram_module):
    """Test the write method handles exceptions gracefully."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop,
        patch(
            "flem.modules.matrix_module.MatrixModule.clear_module"
        ) as mock_clear_module,
        patch("flem.modules.ram_module.logger") as mock_logger,
    ):
        ram_module.running = True

        # Simulate an exception during the write process
        write_queue.side_effect = ValueError("Test exception")
        ram_module.write(update_device, write_queue)

        # Verify that the exception is logged
        mock_logger.exception.assert_called_once_with(
            f"Error while running {ram_module.module_name}: Test exception"
        )

        # Verify that the module is stopped and cleared
        mock_super_stop.assert_called_once()
        mock_clear_module.assert_called_once_with(update_device, write_queue)
