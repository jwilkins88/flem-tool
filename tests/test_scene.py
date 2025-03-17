import pytest
from unittest.mock import MagicMock, patch, call
from threading import Timer, Thread
from flem.matrix.scene import Scene
from flem.models.config import SceneConfig
from flem.modules.matrix_module import MatrixModule


@pytest.fixture
def mock_scene_config():
    """Fixture to create a mock SceneConfig."""
    return SceneConfig(
        name="TestScene",
        show_for=5000,  # 5 seconds
        scene_order=1,
        modules=["Module1", "Module2"],
    )


@pytest.fixture
def mock_modules():
    """Fixture to create mock MatrixModules."""
    module1 = MagicMock(spec=MatrixModule)
    module1.module_name = "Module1"
    module1.is_static = True

    module2 = MagicMock(spec=MatrixModule)
    module2.module_name = "Module2"
    module2.is_static = False

    return [module1, module2]


@pytest.fixture
def mock_callbacks():
    """Fixture to create mock callbacks for update_device, write_queue, and scene_finished."""
    update_device = MagicMock()
    write_queue = MagicMock()
    scene_finished = MagicMock()
    return update_device, write_queue, scene_finished


@pytest.fixture
def scene(mock_scene_config, mock_modules, mock_callbacks):
    """Fixture to create a Scene instance."""
    update_device, write_queue, scene_finished = mock_callbacks
    return Scene(
        config=mock_scene_config,
        modules=mock_modules,
        update_device=update_device,
        write_queue=write_queue,
        scene_finished=scene_finished,
    )


def test_scene_initialization(scene, mock_scene_config, mock_modules):
    """Test the initialization of the Scene class."""
    assert scene.running is False
    assert scene._Scene__config == mock_scene_config
    assert scene._Scene__modules == mock_modules
    assert scene._Scene__threads == []


def test_scene_start(scene, mock_modules, mock_callbacks):
    """Test the start method of the Scene class."""
    update_device, write_queue, scene_finished = mock_callbacks

    with (
        patch("threading.Thread.start") as mock_thread_start,
        patch("threading.Timer.start") as mock_timer_start,
    ):
        scene.start()

        # Verify that the scene is running
        assert scene.running is True

        # Verify that static modules are started directly
        mock_modules[0].start.assert_called_once_with(update_device, write_queue)

        # Verify that non-static modules are started in threads
        mock_thread_start.assert_called_once()

        # Verify that the timer is started
        mock_timer_start.assert_called_once()


def test_scene_start_with_no_timer(scene, mock_scene_config):
    """Test the start method when no timer is required (show_for=0)."""
    mock_scene_config.show_for = 0

    with patch("threading.Thread.start") as mock_thread_start:
        scene.start()

        # Verify that the timer is not created
        assert scene._Scene__timer is None

        # Verify that the scene is running
        assert scene.running is True

        # Verify that threads are started
        mock_thread_start.assert_called()


def test_scene_stop(scene, mock_modules):
    """Test the stop method of the Scene class."""
    mock_thread = MagicMock(spec=Thread)
    mock_thread.is_alive.return_value = True
    mock_timer = MagicMock(spec=Timer)
    mock_timer.is_alive.return_value = True
    scene._Scene__threads = [mock_thread]
    scene._Scene__timer = mock_timer
    scene.stop()

    # Verify that the scene is no longer running
    assert scene.running is False

    # Verify that all modules are stopped
    for module in mock_modules:
        module.stop.assert_called_once()

    # Verify that the timer is joined
    mock_timer.join.assert_called_once_with(5)

    # Verify that threads are joined
    mock_thread.join.assert_called_once()

    # Verify that the thread list is cleared
    assert scene._Scene__threads == []


def test_scene_stop_with_no_timer(scene):
    """Test the stop method when no timer is active."""
    scene._Scene__timer = None

    with patch("threading.Thread.join") as mock_thread_join:
        scene.stop()

        # Verify that the scene is no longer running
        assert scene.running is False

        # Verify that threads are joined
        mock_thread_join.assert_not_called()


def test_scene_stop_with_timer_exception(scene):
    """Test the stop method when the timer join raises an exception."""
    mock_timer = MagicMock(spec=Timer)
    mock_timer.is_alive.return_value = True
    mock_timer.join.side_effect = RuntimeError("Timer join failed")
    scene._Scene__timer = mock_timer

    with patch("flem.matrix.scene.logger") as mock_logger:
        scene.stop()

        # Verify that the exception is logged
        mock_logger.exception.assert_called_once_with(
            f"Error while joining timer for scene {scene._Scene__config.name}: Timer join failed"
        )


def test_scene_stop_with_thread_exception(scene):
    """Test the stop method when a thread join raises an exception."""
    mock_thread = MagicMock(spec=Thread)
    mock_thread.is_alive.return_value = True
    mock_thread.join.side_effect = RuntimeError("Thread join failed")
    scene._Scene__threads = [mock_thread]

    with patch("flem.matrix.scene.logger") as mock_logger:
        scene.stop()

        # Verify that the exception is logged
        mock_logger.error.assert_called_once_with(
            f"Error while joining thread {mock_thread.name}: Thread join failed"
        )
