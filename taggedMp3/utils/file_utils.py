import hashlib

extensions = ['mp4', 'avi']


def md5(file_name):  # used to calculate md5 checksum for file
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def valid_file_extension(filename):  # checking if file is a video file
    if '.' in filename:
        if filename.split('.')[-1] in extensions:
            return True
    return False
