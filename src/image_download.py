import os
import time
import requests
from PIL import Image, UnidentifiedImageError
from db import write_blob


def __get_chunking_data(url: str, chunk_size: int = 1024):
    with requests.get(url, stream=True) as req:
        for chunk in req.iter_content(chunk_size):
            yield chunk


def download_image_as_file(url: str, destination_path: str = './download/'):
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    raw_filename = url.split('/')[-1].split('?')[0]
    basename, ext = os.path.splitext(raw_filename)

    if not ext:
        ext = '.jpg'

    basename = basename + ext
    path_to_image = os.path.join(destination_path, basename)
    path_to_image = path_to_image.replace('*', '')

    with open(path_to_image, 'wb') as f:
        for chunk in __get_chunking_data(url):
            f.write(chunk)

    try:
        Image.open(path_to_image).convert('RGBA').save(path_to_image, 'png')
    except UnidentifiedImageError as e:
        pass
    
    return path_to_image


def download_image_to_db(url: str, title: str, temp_dir: str = './temp/'):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    raw_filename = url.split('/')[-1].split('?')[0]
    basename, ext = os.path.splitext(raw_filename)

    if not ext:
        ext = '.jpg'

    basename = basename + ext
    path_to_image = os.path.join(temp_dir, basename)
    path_to_image = path_to_image.replace('*', '')

    print(f'Downloading {title} ...')
    with open(path_to_image, 'wb') as f:
        for chunk in __get_chunking_data(url):
            f.write(chunk)

    try:
        write_blob(time.time(), title, path_to_image)
        os.remove(path_to_image)
        print('Download completed!')
    except UnidentifiedImageError as e:
        pass

    return path_to_image
