import hashlib
from pathlib import Path
extensions = ['.mp4', '.avi']


def md5(file_name):  # used to calculate md5 checksum for file
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def valid_file_extension(filename):  # checking if file is a video file
    file_path = Path(filename)

    return file_path.suffix in extensions
