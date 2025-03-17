import pytest
from unittest.mock import MagicMock, patch, call
from flem.models.config import ModuleConfig
from flem.modules.matrix_module import MatrixModule


# Create a concrete subclass of MatrixModule for testing
class TestMatrixModule(MatrixModule):
    def __init__(self, config, width, height):
        super().__init__(config, width, height)

    def start(self, update_device, write_queue, execute_callback=True):
        super().start(update_device, write_queue, execute_callback)

    def reset(self):
        pass

    def stop(self):
        super().stop()

    def write(
        self, update_device, write_queue, execute_callback=True, refresh_override=None
    ):
        super().write(update_device, write_queue, execute_callback, refresh_override)

    def clear_module(self, update_device, write_queue):
        super().clear_module(update_device, write_queue)

    def _blink(self, start_row, start_col):
        pass

    def _calculate_pips_to_show(self, value, max_value, max_pips):
        return super()._calculate_pips_to_show(value, max_value, max_pips)

    def _write_array(self, array, start_row, start_col, write_queue):
        super()._write_array(array, start_row, start_col, write_queue)

    def _zero(self, write_queue, start_row, start_col):
        pass

    def _one(self, write_queue, start_row, start_col):
        pass

    def _two(self, write_queue, start_row, start_col):
        pass

    def _three(self, write_queue, start_row, start_col):
        pass

    def _four(self, write_queue, start_row, start_col):
        pass

    def _five(self, write_queue, start_row, start_col):
        pass

    def _six(self, write_queue, start_row, start_col):
        pass

    def _seven(self, write_queue, start_row, start_col):
        pass

    def _eight(self, write_queue, start_row, start_col):
        pass

    def _nine(self, write_queue, start_row, start_col):
        pass

    def _write_object(self, obj, write_queue, start_row, start_col):
        if obj == "0":
            self._zero(write_queue, start_row, start_col)
        else:
            raise ValueError(f"Unknown object: {obj}")


@pytest.fixture
def mock_config():
    """Fixture to create a mock ModuleConfig."""
    return ModuleConfig(
        name="TestModule",
        module_type="TestType",
        position=MagicMock(x=0, y=0),
        refresh_interval=1000,
        arguments={},
    )


@pytest.fixture
def test_module(mock_config):
    """Fixture to create an instance of the TestMatrixModule."""
    return TestMatrixModule(config=mock_config, width=10, height=10)


def test_matrix_module_initialization(mock_config):
    """Test the initialization of the MatrixModule."""
    module = TestMatrixModule(config=mock_config, width=10, height=10)
    assert module.module_name == "TestModule"
    assert module.is_static is False
    assert module.running is True


def test_matrix_module_start(test_module):
    """Test the start method of the MatrixModule."""
    update_device = MagicMock()
    write_queue = MagicMock()
    with (
        patch.object(test_module, "reset") as mock_reset,
        patch.object(test_module, "write") as mock_write,
    ):
        test_module.start(update_device, write_queue)
        assert test_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_matrix_module_stop(test_module):
    """Test the stop method of the MatrixModule."""
    test_module.stop()
    assert test_module.running is False


def test_matrix_module_write(test_module):
    """Test the write method of the MatrixModule."""
    update_device = MagicMock()
    write_queue = MagicMock()
    with patch("time.sleep") as mock_sleep:
        test_module.write(update_device, write_queue, execute_callback=True)
        update_device.assert_called_once()


def test_matrix_module_clear_module(test_module):
    """Test the clear_module method of the MatrixModule."""
    update_device = MagicMock()
    write_queue = MagicMock()
    test_module.clear_module(update_device, write_queue)
    update_device.assert_called_once()
    write_queue.assert_has_calls(
        [call((col, row, False)) for row in range(10) for col in range(10)]
    )


def test_matrix_module_write_object(test_module):
    """Test the _write_object method of the MatrixModule."""
    write_queue = MagicMock()
    with patch.object(test_module, "_zero") as mock_zero:
        test_module._write_object("0", write_queue, 0, 0)
        mock_zero.assert_called_once_with(write_queue, 0, 0)


def test_matrix_module_write_object_unknown(test_module):
    """Test the _write_object method with an unknown object."""
    write_queue = MagicMock()
    with patch("flem.modules.matrix_module.logger") as mock_logger:
        with pytest.raises(ValueError, match="Unknown object: unknown"):
            test_module._write_object("unknown", write_queue, 0, 0)
            test_module._write_object("unknown", write_queue, 0, 0)
