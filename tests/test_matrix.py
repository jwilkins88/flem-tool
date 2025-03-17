import pytest
from unittest.mock import MagicMock, patch, call
from flem.matrix.matrix import Matrix
from flem.devices.led_device import LedDevice
from flem.models.config import SceneConfig
from flem.modules.matrix_module import MatrixModule
from flem.matrix.scene import Scene


@pytest.fixture
def mock_led_device():
    """Fixture to create a mock LedDevice."""
    device = MagicMock(spec=LedDevice)
    device.WIDTH = 8
    device.HEIGHT = 8
    device.OFF = 0
    device.name = "TestMatrix"
    device.is_open.return_value = False
    return device


@pytest.fixture
def mock_scene_config():
    """Fixture to create a mock SceneConfig."""
    return SceneConfig(
        name="TestScene",
        show_for=10,
        scene_order=1,
        modules=["Module1", "Module2"],
    )


@pytest.fixture
def mock_matrix_modules():
    """Fixture to create mock MatrixModules."""
    module1 = MagicMock(spec=MatrixModule)
    module1.module_name = "Module1"
    module2 = MagicMock(spec=MatrixModule)
    module2.module_name = "Module2"
    return [module1, module2]


@pytest.fixture
def mock_scenes():
    """Fixture to create mock Scenes."""
    scene1 = MagicMock(spec=Scene)
    scene2 = MagicMock(spec=Scene)
    return [scene1, scene2]


def test_matrix_initialization(mock_led_device, mock_scene_config, mock_matrix_modules):
    """Test the initialization of the Matrix class."""
    matrix = Matrix(
        matrix_device=mock_led_device,
        modules=mock_matrix_modules,
        scenes=[mock_scene_config],
    )

    assert matrix.name == "TestMatrix"
    assert matrix.running is True
    assert len(matrix._Matrix__scenes) == 1
    assert isinstance(matrix._Matrix__scenes[0], Scene)
    mock_led_device.connect.assert_called_once()


def test_matrix_start(mock_led_device, mock_scene_config, mock_matrix_modules):
    """Test starting the Matrix."""
    matrix = Matrix(
        matrix_device=mock_led_device,
        modules=mock_matrix_modules,
        scenes=[mock_scene_config],
    )

    with patch("threading.Thread.start") as mock_thread_start:
        matrix.start()
        assert matrix.running is True
        mock_thread_start.assert_called_once()


def test_matrix_set_matrix(mock_led_device, mock_scene_config, mock_matrix_modules):
    """Test setting the matrix."""
    matrix = Matrix(
        matrix_device=mock_led_device,
        modules=mock_matrix_modules,
        scenes=[mock_scene_config],
    )

    new_matrix = [
        [1 for _ in range(mock_led_device.HEIGHT)] for _ in range(mock_led_device.WIDTH)
    ]
    with patch.object(matrix, "_Matrix__update_device") as mock_update_device:
        matrix.set_matrix(new_matrix)
        assert matrix._matrix == new_matrix
        mock_update_device.assert_called_once()


def test_matrix_run_next_scene(
    mock_led_device, mock_scene_config, mock_matrix_modules, mock_scenes
):
    """Test running the next scene."""
    matrix = Matrix(
        matrix_device=mock_led_device,
        modules=mock_matrix_modules,
        scenes=[mock_scene_config],
    )
    matrix._Matrix__scenes = mock_scenes
    matrix._Matrix__current_scene = 0

    matrix.run_next_scene()
    mock_scenes[0].start.assert_called_once()


def test_matrix_reset_matrix(mock_led_device, mock_scene_config, mock_matrix_modules):
    """Test resetting the matrix."""
    matrix = Matrix(
        matrix_device=mock_led_device,
        modules=mock_matrix_modules,
        scenes=[mock_scene_config],
    )

    with patch.object(matrix, "_Matrix__update_device") as mock_update_device:
        matrix.reset_matrix()
        assert matrix._matrix == matrix._Matrix__DEFAULT_MATRIX
        mock_update_device.assert_called_once()


def test_matrix_stop(
    mock_led_device, mock_scene_config, mock_matrix_modules, mock_scenes
):
    """Test stopping the Matrix."""
    matrix = Matrix(
        matrix_device=mock_led_device,
        modules=mock_matrix_modules,
        scenes=[mock_scene_config],
    )
    matrix._Matrix__scenes = mock_scenes
    matrix._Matrix__thread = MagicMock()

    with patch.object(matrix, "reset_matrix") as mock_reset_matrix:
        matrix.stop()
        assert matrix.running is False
        for scene in mock_scenes:
            scene.stop.assert_called_once()
        matrix._Matrix__thread.join.assert_called_once()
        mock_reset_matrix.assert_called_once()
        mock_led_device.close.assert_called_once()


def test_matrix_update_device(mock_led_device, mock_scene_config, mock_matrix_modules):
    """Test updating the device."""
    matrix = Matrix(
        matrix_device=mock_led_device,
        modules=mock_matrix_modules,
        scenes=[mock_scene_config],
    )

    with (
        patch.object(matrix._Matrix__change_queue, "get", return_value=(0, 0, 1)),
        patch.object(matrix._Matrix__change_queue, "empty", side_effect=[False, True]),
        patch.object(matrix._Matrix__change_queue, "task_done") as mock_task_done,
    ):
        matrix._Matrix__update_device()
        assert matrix._matrix[0][0] == 1
        mock_task_done.assert_called_once()
        mock_led_device.render_matrix.assert_called_once_with(matrix._matrix)


def test_matrix_str(mock_led_device, mock_scene_config, mock_matrix_modules):
    """Test the string representation of the Matrix."""
    matrix = Matrix(
        matrix_device=mock_led_device,
        modules=mock_matrix_modules,
        scenes=[mock_scene_config],
    )

    result = str(matrix)
    assert isinstance(result, str)
    assert (
        result
        == "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛\n⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛\n⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛\n⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛\n⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛\n⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛\n⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛\n⬛ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⬛\n⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛"
    )
