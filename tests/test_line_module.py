import pytest
from unittest.mock import MagicMock, patch, call
from flem.modules.line_module import LineModule
from flem.models.modules.line_config import LineConfig, LineConfigArguments
from flem.models.config import ModulePositionConfig
from flem.modules.matrix_module import MatrixModule


def stop_module(module: MatrixModule):
    """Helper function to stop the module's loop."""
    module.running = False


@pytest.fixture
def mock_line_config():
    """Fixture to create a mock LineConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = LineConfigArguments(line_style="solid", width=9)
    return LineConfig(
        name="TestLine",
        module_type="Line",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )


@pytest.fixture
def line_module(mock_line_config):
    """Fixture to create a LineModule instance."""
    return LineModule(config=mock_line_config)


def test_line_module_initialization(mock_line_config):
    """Test the initialization of LineModule."""
    module = LineModule(config=mock_line_config, width=9, height=1)

    assert module.module_name == "TestLine"
    assert module._LineModule__config == mock_line_config


def test_line_module_initialization_with_invalid_config():
    """Test LineModule initialization with an invalid config."""
    invalid_config = MagicMock()
    with patch("flem.models.modules.line_config.LineConfigSchema.load") as mock_load:
        mock_load.return_value = MagicMock()
        module = LineModule(config=invalid_config, width=9, height=1)

        mock_load.assert_called_once()
        assert module._LineModule__config is not None


def test_line_module_start(line_module):
    """Test the start method of LineModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch.object(line_module, "reset") as mock_reset,
        patch.object(line_module, "write") as mock_write,
    ):
        line_module.start(update_device, write_queue)

        assert line_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_line_module_stop(line_module):
    """Test the stop method of LineModule."""
    with patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop:
        line_module.stop()

        assert line_module.running is False
        mock_super_stop.assert_called_once()


def test_line_module_write_solid_line(line_module):
    """Test the write method for a solid line."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write:
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )

        line_module.running = True
        line_module.write(update_device, write_queue)

        # Verify that all pixels in the line are written as `True`
        expected_calls = [
            call((i, line_module._LineModule__config.position.y, True))
            for i in range(
                line_module._LineModule__config.position.x,
                line_module._LineModule__config.position.x
                + line_module._LineModule__config.arguments.width,
            )
        ]
        write_queue.assert_has_calls(expected_calls, any_order=False)

        # Verify that the parent class's write method is called
        mock_super_write.assert_called_once_with(update_device, write_queue, True, None)


def test_line_module_write_dashed_line(mock_line_config):
    """Test the write method for a dashed line."""
    mock_line_config.arguments.line_style = "dashed"
    line_module = LineModule(config=mock_line_config, width=9, height=1)
    update_device = MagicMock()
    write_queue = MagicMock()

    with patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write:
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )

        line_module.running = True
        line_module.write(update_device, write_queue)

        # Verify that pixels alternate between `True` and `False` for a dashed line
        expected_calls = []
        for i in range(line_module._LineModule__config.arguments.width):
            if i % 2 != 0:
                expected_calls.append(
                    call((i, line_module._LineModule__config.position.y, False))
                )
            else:
                expected_calls.append(
                    call((i, line_module._LineModule__config.position.y, True))
                )

        write_queue.assert_has_calls(expected_calls, any_order=False)

        # Verify that the parent class's write method is called
        mock_super_write.assert_called_once_with(update_device, write_queue, True, None)


def test_line_module_write_handles_exceptions(line_module):
    """Test the write method handles exceptions gracefully."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop,
        patch(
            "flem.modules.matrix_module.MatrixModule.clear_module"
        ) as mock_clear_module,
        patch("flem.modules.line_module.logger") as mock_logger,
    ):
        line_module.running = True

        # Simulate an exception during the write process
        write_queue.side_effect = ValueError("Test exception")
        line_module.write(update_device, write_queue)

        # Verify that the exception is logged
        mock_logger.exception.assert_called_once_with(
            f"Error while running {line_module.module_name}: Test exception"
        )

        # Verify that the module is stopped and cleared
        mock_super_stop.assert_called_once()
        mock_clear_module.assert_called_once_with(update_device, write_queue)
