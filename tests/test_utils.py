import os

from samer.utils import get_tuple_list_env
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

admins_test = "('admin_test','admin');('admin_test2','admin')"


def test_is_image():
    with open(image_path, "rb") as file:
        file_bytes = file.read()
        assert is_image(file_bytes)


def test_is_video():
    with open(video_path, "rb") as file:
        file_bytes = file.read()
        assert is_video(file_bytes)


def test_get_tuple_list_env():
    admin_tuples = get_tuple_list_env(admins_test)
    assert isinstance(admin_tuples, list)
    assert len(admin_tuples) == 2
    assert admin_tuples[0] == ("admin_test", "admin")
    assert admin_tuples[1] == ("admin_test2", "admin")
