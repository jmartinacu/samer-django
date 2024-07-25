import os

from samer.posts.utils import is_image, is_video

image_path = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "image-test.jpeg",
)

video_path = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "video-test.mp4",
)


def test_is_image():
    with open(image_path, "rb") as file:
        file_bytes = file.read()
        assert is_image(file_bytes)


def test_is_video():
    with open(video_path, "rb") as file:
        file_bytes = file.read()
        assert is_video(file_bytes)
