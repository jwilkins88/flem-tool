import os
import shutil
import pytest
from unittest.mock import MagicMock, patch, mock_open
from flem.utilities.utilities import (
    __CONFIG_PATHS,
    create_animator_files,
    check_and_create_user_directory,
    get_config_location,
    load_module,
    get_config,
    read_config_from_file,
    has_config_changed,
    run_matrices_from_config,
    parse_int,
)
from flem.models.config import Config, ModuleConfig
from flem.matrix.matrix import Matrix
from flem.devices.led_device import LedDevice


def test_create_animator_files():
    """Test the creation of animator files."""
    with (
        patch("os.path.exists", return_value=False),
        patch("os.makedirs") as mock_makedirs,
        patch("shutil.copytree") as mock_copytree,
    ):
        create_animator_files()
        mock_makedirs.assert_called_once()
        mock_copytree.assert_not_called()


def test_create_animator_files_directory_exists():
    """Test the creation of animator files when the directory already exists."""
    with (
        patch("os.path.exists", return_value=True),
        patch("os.makedirs") as mock_makedirs,
        patch("shutil.copytree") as mock_copytree,
    ):
        create_animator_files()
        mock_makedirs.assert_not_called()
        mock_copytree.assert_called_once()


def test_check_and_create_user_directory():
    """Test the creation of the user directory."""
    with (
        patch("os.path.exists", side_effect=[False, True]),
        patch("os.makedirs") as mock_makedirs,
        patch("builtins.open", mock_open()) as mock_file,
    ):
        check_and_create_user_directory()
        mock_makedirs.assert_called_once()
        mock_file.call_count == 2


def test_check_and_create_user_directory_exists():
    """Test when the user directory already exists."""
    with (
        patch("os.path.exists", return_value=True),
        patch("os.makedirs") as mock_makedirs,
        patch("builtins.open", mock_open()) as mock_file,
    ):
        check_and_create_user_directory()
        mock_makedirs.assert_not_called()
        mock_file.assert_not_called()


def test_load_module():
    """Test loading a module."""
    module_config = ModuleConfig(
        module_type="TestModule",
        name="test_module",
        arguments={},
        position={
            "x": 0,
            "y": 0,
        },
        refresh_interval=0,
    )
    with (
        patch("os.path.join", return_value="test_module.py"),
        patch("os.path.isfile", return_value=True),
        patch("glob.glob", return_value=["test_module.py"]),
        patch("builtins.open", mock_open(read_data="")),
        patch("importlib.import_module") as mock_import_module,
    ):
        mock_class = MagicMock()
        setattr(mock_import_module.return_value, "TestModule", mock_class)
        # mock_import_module.return_value.TestModule = mock_class
        result = load_module(module_config)
        assert result == mock_class.return_value


def test_load_module_directory_not_found():
    """Test loading a module when the directory does not exist."""
    module_config = ModuleConfig(
        module_type="NonExistentModule",
        name="non_existent_module",
        arguments={},
        position={
            "x": 0,
            "y": 0,
        },
        refresh_interval=0,
    )
    with (
        patch("os.path.join", return_value="non_existent_module.py"),
        patch("os.path.isfile", return_value=False),
        patch("glob.glob", return_value=[]),
    ):
        result = load_module(module_config)
        assert result is None


def test_get_config():
    """Test retrieving the configuration."""
    mock_config_string = '{"devices": []}'
    with (
        patch(
            "flem.utilities.utilities.read_config_from_file",
            return_value=mock_config_string,
        ),
        patch("flem.utilities.utilities.ConfigSchema") as mock_config_schema,
    ):
        mock_config = MagicMock()
        mock_config_schema.return_value.loads.return_value = mock_config
        config, config_hash = get_config()
        assert config == mock_config
        assert config_hash is not None


def test_read_config_from_file():
    """Test reading the configuration from a file."""
    mock_file_content = '{"devices": []}'
    with (
        patch("os.path.exists", side_effect=[False, True]),
        patch("builtins.open", mock_open(read_data=mock_file_content)) as mock_file,
    ):
        result = read_config_from_file()
        assert result == mock_file_content
        mock_file.assert_called_once()


def test_read_config_from_file_not_found():
    """Test reading the configuration when no file is found."""
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            read_config_from_file()


def test_has_config_changed():
    """Test checking if the configuration has changed."""
    current_hash = "abc123"
    new_config = '{"devices": []}'
    with patch("flem.utilities.utilities.md5") as mock_md5:
        mock_md5.return_value.hexdigest.side_effect = ["def456"]
        result = has_config_changed(current_hash, new_config)
        assert result is True


def test_has_config_has_not_changed():
    """Test checking if the configuration has not changed."""
    current_hash = "abc123"
    new_config = '{"devices": []}'
    with patch("flem.utilities.utilities.md5") as mock_md5:
        mock_md5.return_value.hexdigest.side_effect = ["abc123"]
        result = has_config_changed(current_hash, new_config)
        assert result is False


def test_run_matrices_from_config():
    """Test running matrices from the configuration."""
    mock_config = MagicMock(devices=[MagicMock(name="Device1", modules=[], scenes=[])])
    mock_matrix = MagicMock()
    with (
        patch("flem.utilities.utilities.LedDevice") as mock_led_device,
        patch(
            "flem.utilities.utilities.Matrix", return_value=mock_matrix
        ) as mock_matrix_class,
    ):
        result = run_matrices_from_config(mock_config, [])
        assert len(result) == 1
        mock_led_device.assert_called_once()
        mock_matrix_class.assert_called_once()
        mock_matrix.start.assert_called_once()


def test_run_matrices_from_config_matrix_already_running():
    """Test running matrices from the configuration when a matrix is already running."""
    mock_config = MagicMock(devices=[MagicMock(name="Device1", modules=[], scenes=[])])
    mock_matrix = MagicMock()
    mock_matrix.is_running = True  # Simulate that the matrix is already running
    with (
        patch("flem.utilities.utilities.LedDevice") as mock_led_device,
        patch(
            "flem.utilities.utilities.Matrix", return_value=mock_matrix
        ) as mock_matrix_class,
    ):
        result = run_matrices_from_config(mock_config, [mock_matrix])
        assert len(result) == 1
        mock_led_device.assert_called_once()
        mock_matrix_class.assert_called_once()
        mock_matrix.stop.assert_called_once()  # Ensure the matrix is stopped before restarting
        mock_matrix.start.assert_called_once()


@pytest.mark.parametrize(
    "value,expected",
    [
        ("123", 123),
        ("abc", None),
        ("", None),
        ("-456", -456),
    ],
)
def test_parse_int(value, expected):
    """Test parsing a string to an integer."""
    result = parse_int(value)
    assert result == expected


def test_get_config_location_found():
    """Test finding the configuration file in predefined paths."""
    with patch("os.path.exists", side_effect=[False, True]) as mock_exists:
        result = get_config_location()
        assert result == "config.json"
        assert mock_exists.call_count == 2


def test_get_config_location_not_found():
    """Test when no configuration file is found in predefined paths."""
    with patch("os.path.exists", return_value=False) as mock_exists:
        result = get_config_location()
        assert result is None
        assert mock_exists.call_count == len(__CONFIG_PATHS)
