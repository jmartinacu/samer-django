import subprocess
import os
import tempfile
from io import BytesIO

import magic
import requests
import imageio
from PIL import Image

from samer.utils import upload_file, delete_file


def upload_thumbnail(frame: int, video_url: str):
    command = [
        "ffmpeg",
        "-i",
        video_url,
        "-vf",
        f"select='eq(n,{frame})'",
        "-q:v",
        "3",
        "-f",
        "image2pipe",
        "-vcodec",
        "mjpeg",
        "pipe:1",
    ]
    process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if process.returncode != 0:
        raise Exception(f"ffmpeg error: {process.stderr.decode('utf-8')}")
    video_name = video_url.split("/")[-1]
    thumb_name, _thumb_ext = os.path.splitext(video_name)
    thumb_io = BytesIO(process.stdout)
    thumbnail_url = upload_file(
        file=thumb_io, object_name=f"videos/thumbnails/{thumb_name}.jpg"
    )
    return thumbnail_url


def delete_thumbnail(thumbnail_url: str):
    thumbnail_name = thumbnail_url.split("/")[-1]
    thumbnail_object_name = f"videos/thumbnails/{thumbnail_name}"
    delete_file(thumbnail_object_name)


def get_mime_type_from_urls(urls: list[str]) -> list[str] | str:
    result = None
    result = []
    for url in urls:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        mime = magic.Magic(mime=True)
        result.append(mime.from_buffer(response.raw.read(1024)))
        response.close()
    return result


def is_image(file_bytes):
    try:
        Image.open(BytesIO(file_bytes))
        return True
    except IOError:
        return False


def is_video(file_bytes):
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".mp4",
            delete=True,
        ) as temp_file:
            temp_file.write(file_bytes)
            temp_file.flush()
            reader = imageio.get_reader(temp_file.name)
            try:
                _ = reader.get_next_data()
                is_video_file = True
            except RuntimeError:
                is_video_file = False
            reader.close()
            return is_video_file

    except Exception as e:
        print(f"Exception occurred: {e}")
        return False
