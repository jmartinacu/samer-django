import subprocess
from os import path
from io import BytesIO

import magic
import requests

from samer.utils import upload_file


def upload_thumbnail(frame: int, video_url: str):
    command = [
        'ffmpeg',
        '-i', video_url,
        '-vf', f'select=eq(n\,{frame})',  # pylint: disable=W1401
        '-q:v', '3',
        '-f', 'image2pipe',
        '-vcodec', 'mjpeg',
        'pipe:1'
    ]
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False
    )
    if process.returncode != 0:
        raise Exception(  # pylint: disable=W0719
            f"ffmpeg error: {process.stderr.decode('utf-8')}"  # pylint: disable=W0719
        )  # pylint: disable=W0719
    video_name = video_url.split('/')[-1]
    thumb_name, _thumb_ext = path.splitext(video_name)
    thumb_io = BytesIO(process.stdout)
    thumbnail_url = upload_file(
        file=thumb_io, object_name=f'videos/thumbnails/{thumb_name}.jpg'
    )
    return thumbnail_url


def get_mime_type_from_url(url):
    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(response.raw.read(1024))
    response.close()
    return mime_type
