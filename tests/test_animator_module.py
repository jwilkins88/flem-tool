import pytest
from unittest.mock import MagicMock, patch, call, mock_open
from flem.modules.animator_module import AnimatorModule
from flem.models.modules.animator_config import AnimatorConfig, AnimatorConfigArguments
from flem.models.config import ModulePositionConfig
from flem.modules.matrix_module import MatrixModule


def stop_module(module: MatrixModule):
    module.running = False


@pytest.fixture
def mock_animator_config():
    """Fixture to create a mock AnimatorConfig."""
    position = ModulePositionConfig(x=0, y=0)
    arguments = AnimatorConfigArguments(
        frames=[],
        width=6,
        height=4,
        animation_file=None,
    )
    return AnimatorConfig(
        name="TestAnimator",
        module_type="Animator",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )


@pytest.fixture
def animator_module(mock_animator_config):
    """Fixture to create an AnimatorModule instance."""
    return AnimatorModule(config=mock_animator_config, width=6, height=4)


def test_animator_module_initialization(mock_animator_config):
    """Test the initialization of AnimatorModule."""
    module = AnimatorModule(config=mock_animator_config, width=6, height=4)

    assert module.module_name == "TestAnimator"
    assert module._AnimatorModule__config == mock_animator_config


def test_animator_module_initialization_with_invalid_config():
    """Test AnimatorModule initialization with an invalid config."""
    invalid_config = MagicMock()
    with patch(
        "flem.models.modules.animator_config.AnimatorConfigSchema.load"
    ) as mock_load:
        mock_load.return_value = MagicMock()
        module = AnimatorModule(config=invalid_config, width=6, height=4)

        mock_load.assert_called_once()
        assert module._AnimatorModule__config is not None


def test_animator_module_load_animation_file(mock_animator_config):
    """Test loading animation frames from a file."""
    mock_animator_config.arguments.animation_file = "test_animation.json"
    with (
        patch(
            "builtins.open",
            mock_open(read_data='[{"frame": [[1, 0], [0, 1]], "frame_duration": 500}]'),
        ),
        patch(
            "flem.models.modules.animator_config.AnimatorFrameSchema.loads"
        ) as mock_loads,
    ):
        mock_loads.return_value = [{"frame": [[1, 0], [0, 1]], "frame_duration": 500}]
        module = AnimatorModule(config=mock_animator_config, width=6, height=4)

        mock_loads.assert_called_once()
        assert len(module._AnimatorModule__config.arguments.frames) == 1


def test_animator_module_start(animator_module):
    """Test the start method of AnimatorModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    with (
        patch.object(animator_module, "reset") as mock_reset,
        patch.object(animator_module, "write") as mock_write,
    ):
        animator_module.start(update_device, write_queue)

        assert animator_module.running is True
        mock_reset.assert_called_once()
        mock_write.assert_called_once_with(update_device, write_queue, True)


def test_animator_module_stop(animator_module):
    """Test the stop method of AnimatorModule."""
    with patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop:
        animator_module.stop()

        assert animator_module.running is False
        mock_super_stop.assert_called_once()


def test_animator_module_write(animator_module):
    """Test the write method of AnimatorModule."""
    update_device = MagicMock()
    write_queue = MagicMock()

    animator_module._AnimatorModule__config.arguments.frames = [
        MagicMock(frame=[[1, 0], [0, 1]], frame_duration=500)
    ]

    with (
        patch.object(animator_module, "_write_array") as mock_write_array,
        patch("flem.modules.matrix_module.MatrixModule.write") as mock_super_write,
    ):
        mock_super_write.configure_mock(
            **{"return_value": None, "side_effect": stop_module}
        )
        animator_module.running = True
        animator_module.write(update_device, write_queue)
        mock_write_array.assert_called_once_with(
            [[1, 0], [0, 1]],
            animator_module._AnimatorModule__config.position.x,
            animator_module._AnimatorModule__config.position.y,
            write_queue,
        )
        mock_super_write.assert_called_once_with(
            update_device, write_queue, True, 500, True
        )


def test_animator_module_write_handles_exceptions(animator_module):
    """Test the write method handles exceptions gracefully."""
    update_device = MagicMock()
    write_queue = MagicMock()

    animator_module._AnimatorModule__config.arguments.frames = []

    with (
        patch("flem.modules.matrix_module.MatrixModule.stop") as mock_super_stop,
        patch(
            "flem.modules.matrix_module.MatrixModule.clear_module"
        ) as mock_clear_module,
        patch("flem.modules.animator_module.logger") as mock_logger,
    ):
        animator_module.running = True
        animator_module.write(update_device, write_queue)

        mock_logger.exception.assert_called_once()
        mock_super_stop.assert_called_once()
        mock_clear_module.assert_called_once_with(update_device, write_queue)
