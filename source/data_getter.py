from pathlib import Path
from zipfile import ZipFile
from urllib3 import PoolManager

data_folder_path = Path().absolute().parent / 'data'
version_number = "0.18.47"
file_type = ".zip"
file_name = version_number + file_type


def change_file(version_string, extension_string='.zip'):
    global version_number
    global file_type
    global file_name

    version_number = version_string
    file_type = extension_string
    file_name = version_number + file_type


def set_new_version(version_string):
    global version_number

    version_number = version_string
    change_file(version_number)


# todo version changer, maybe have a dropdown box
def download_file():
    base_url = "https://github.com/wube/factorio-data/archive/"

    # https: // stackoverflow.com / a / 7244263 / 2295388
    import urllib.request
    import shutil

    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(base_url + version_number + file_type) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def read_data_from_zip():
    with ZipFile(file_name + '.zip', 'r') as my_zip:
        text_stream = my_zip.read('factorio-data-' + version_number + '/base/prototypes/recipe/recipe.lua')
        return text_stream


# todo recipe data parser - parse data from lua into base classes, maybe have classes handle it themselves

def data_extender(text_stream):
    check_text = b'data:extend(\n{'
    if not text_stream.startswith(check_text):
        print("not data file")
        return None
    text_stream = text_stream.partition(check_text)[2]
    for data_line in text_stream.split(b'\n  {\n    '):
        print(data_line)
        for line in data_line.split(b'\n    '):
            print(line.partition(B' = '))


# data_extender(read_data_from_zip())

# https://note.nkmk.me/en/python-check-int-float/
def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


# https://stackoverflow.com/questions/645312/what-is-the-quickest-way-to-http-get-in-python/54856660#54856660
def get_current_version():
    http = PoolManager()
    r = http.request('GET', 'https://raw.githubusercontent.com/wube/factorio-data/master/base/info.json')
    line = r.data.decode('utf-8').split('  "version": "')[1]
    return line.split('"')[0]


def get_all_versions():
    versions = list()
    versions.append(get_current_version())
    base_url = 'https://github.com/wube/factorio-data/releases'
    url = base_url
    split_string = '<a href="/wube/factorio-data/releases/tag/'

    while versions[-1] != '0.5.0':  # first version released
        http = PoolManager()
        r = http.request('GET', url)
        for line in r.data.decode('utf-8').split(split_string):  # maybe swap to a generator
            if is_integer(line[0]):
                versions.append(line.split('"')[0])
        url = base_url + '?after=' + versions[-1]
    return versions
