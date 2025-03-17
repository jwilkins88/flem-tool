import pytest
from marshmallow import ValidationError
from flem.models.modules.animator_config import (
    AnimatorFrame,
    AnimatorConfigArguments,
    AnimatorConfig,
    AnimatorFrameSchema,
    AnimatorConfigArgumentsSchema,
    AnimatorConfigSchema,
)
from flem.models.config import ModulePositionConfig


def test_animator_frame_initialization():
    """Test the initialization of AnimatorFrame."""
    frame = [[1, 0, 1], [0, 1, 0]]
    frame_duration = 500
    animator_frame = AnimatorFrame(frame=frame, frame_duration=frame_duration)

    assert animator_frame.frame == frame
    assert animator_frame.frame_duration == frame_duration


def test_animator_config_arguments_initialization():
    """Test the initialization of AnimatorConfigArguments."""
    frame1 = AnimatorFrame(frame=[[1, 0], [0, 1]], frame_duration=500)
    frame2 = AnimatorFrame(frame=[[0, 1], [1, 0]], frame_duration=300)
    frames = [frame1, frame2]
    width = 2
    height = 2
    animation_file = "test_animation.json"

    arguments = AnimatorConfigArguments(
        frames=frames, width=width, height=height, animation_file=animation_file
    )

    assert arguments.frames == frames
    assert arguments.width == width
    assert arguments.height == height
    assert arguments.animation_file == animation_file


def test_animator_config_initialization():
    """Test the initialization of AnimatorConfig."""
    position = ModulePositionConfig(x=0, y=0)
    frame1 = AnimatorFrame(frame=[[1, 0], [0, 1]], frame_duration=500)
    frame2 = AnimatorFrame(frame=[[0, 1], [1, 0]], frame_duration=300)
    frames = [frame1, frame2]
    arguments = AnimatorConfigArguments(
        frames=frames, width=2, height=2, animation_file="test_animation.json"
    )

    config = AnimatorConfig(
        name="TestAnimator",
        module_type="Animator",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )

    assert config.name == "TestAnimator"
    assert config.module_type == "Animator"
    assert config.position == position
    assert config.refresh_interval == 1000
    assert config.arguments == arguments


def test_animator_frame_schema_load():
    """Test loading data into AnimatorFrame using AnimatorFrameSchema."""
    data = {"frame": [[1, 0], [0, 1]], "frame_duration": 500}
    schema = AnimatorFrameSchema()
    result = schema.load(data)

    assert isinstance(result, AnimatorFrame)
    assert result.frame == data["frame"]
    assert result.frame_duration == data["frame_duration"]


def test_animator_frame_schema_dump():
    """Test dumping AnimatorFrame data using AnimatorFrameSchema."""
    frame = AnimatorFrame(frame=[[1, 0], [0, 1]], frame_duration=500)
    schema = AnimatorFrameSchema()
    result = schema.dump(frame)

    assert result == {"frame": [[1, 0], [0, 1]], "frame_duration": 500}


def test_animator_config_arguments_schema_load():
    """Test loading data into AnimatorConfigArguments using AnimatorConfigArgumentsSchema."""
    data = {
        "frames": [
            {"frame": [[1, 0], [0, 1]], "frame_duration": 500},
            {"frame": [[0, 1], [1, 0]], "frame_duration": 300},
        ],
        "width": 2,
        "height": 2,
        "animation_file": "test_animation.json",
    }
    schema = AnimatorConfigArgumentsSchema()
    result = schema.load(data)

    assert isinstance(result, AnimatorConfigArguments)
    assert len(result.frames) == 2
    assert result.frames[0].frame == [[1, 0], [0, 1]]
    assert result.frames[0].frame_duration == 500
    assert result.width == 2
    assert result.height == 2
    assert result.animation_file == "test_animation.json"


def test_animator_config_arguments_schema_dump():
    """Test dumping AnimatorConfigArguments data using AnimatorConfigArgumentsSchema."""
    frame1 = AnimatorFrame(frame=[[1, 0], [0, 1]], frame_duration=500)
    frame2 = AnimatorFrame(frame=[[0, 1], [1, 0]], frame_duration=300)
    arguments = AnimatorConfigArguments(
        frames=[frame1, frame2], width=2, height=2, animation_file="test_animation.json"
    )
    schema = AnimatorConfigArgumentsSchema()
    result = schema.dump(arguments)

    assert result == {
        "frames": [
            {"frame": [[1, 0], [0, 1]], "frame_duration": 500},
            {"frame": [[0, 1], [1, 0]], "frame_duration": 300},
        ],
        "width": 2,
        "height": 2,
        "animation_file": "test_animation.json",
    }


def test_animator_config_schema_load():
    """Test loading data into AnimatorConfig using AnimatorConfigSchema."""
    data = {
        "name": "TestAnimator",
        "module_type": "Animator",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {
            "frames": [
                {"frame": [[1, 0], [0, 1]], "frame_duration": 500},
                {"frame": [[0, 1], [1, 0]], "frame_duration": 300},
            ],
            "width": 2,
            "height": 2,
            "animation_file": "test_animation.json",
        },
    }
    schema = AnimatorConfigSchema()
    result = schema.load(data)

    assert isinstance(result, AnimatorConfig)
    assert result.name == "TestAnimator"
    assert result.module_type == "Animator"
    assert result.position.x == 0
    assert result.position.y == 0
    assert result.refresh_interval == 1000
    assert len(result.arguments.frames) == 2
    assert result.arguments.frames[0].frame == [[1, 0], [0, 1]]
    assert result.arguments.frames[0].frame_duration == 500


def test_animator_config_schema_dump():
    """Test dumping AnimatorConfig data using AnimatorConfigSchema."""
    position = ModulePositionConfig(x=0, y=0)
    frame1 = AnimatorFrame(frame=[[1, 0], [0, 1]], frame_duration=500)
    frame2 = AnimatorFrame(frame=[[0, 1], [1, 0]], frame_duration=300)
    arguments = AnimatorConfigArguments(
        frames=[frame1, frame2], width=2, height=2, animation_file="test_animation.json"
    )
    config = AnimatorConfig(
        name="TestAnimator",
        module_type="Animator",
        position=position,
        refresh_interval=1000,
        arguments=arguments,
    )
    schema = AnimatorConfigSchema()
    result = schema.dump(config)

    assert result == {
        "name": "TestAnimator",
        "module_type": "Animator",
        "position": {"x": 0, "y": 0},
        "refresh_interval": 1000,
        "arguments": {
            "frames": [
                {"frame": [[1, 0], [0, 1]], "frame_duration": 500},
                {"frame": [[0, 1], [1, 0]], "frame_duration": 300},
            ],
            "width": 2,
            "height": 2,
            "animation_file": "test_animation.json",
        },
    }
