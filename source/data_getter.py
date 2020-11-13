from pathlib import Path
from zipfile import ZipFile

from urllib3 import PoolManager
from urllib3.exceptions import MaxRetryError


class Data(object):
    data_folder_path = Path().absolute().parent / 'data'
    latest_version = '0.5.0'
    suffixes = ['demo-recipe', 'capsule', 'circuit-network', 'demo-furnace-recipe', 'demo-recipe',
                'demo-turret', 'equipment', 'fluid-recipe', 'inserter', 'module', 'recipe', 'turret']

    def __init__(self, version_number='0.5.0', file_type='.zip'):
        self.version_number = version_number
        self.file_type = file_type
        try:
            Data.latest_version = Data.get_latest_version()
        except MaxRetryError:
            # when no connection
            # todo have a function to get the latest version in data folder
            Data.latest_version = '1.0.0'
        # Data.download_file(Data.latest_version)

    # todo version changer, maybe have a dropdown box
    def set_new_version(self, version_string):
        self.version_number = version_string

    @property
    def file_name(self):
        return self.version_number + self.file_type

    @staticmethod
    def download_file(version_num, file_type='.zip'):
        base_url = 'https://github.com/wube/factorio-data/archive/'
        out_name = 'factorio-data-' + version_num + file_type
        out_path = Data.data_folder_path / out_name

        if Path.exists(out_path):
            # todo check if user wants to overwrite
            raise FileExistsError("File is already downloaded")
        else:
            # https: // stackoverflow.com / a / 7244263 / 2295388
            import urllib.request
            import shutil
            # current versions download file is 'master'
            if Data.latest_version == version_num:
                file_name = 'master' + file_type
            else:
                file_name = version_num + file_type

            # Download the file from url and save it locally under out_path
            with urllib.request.urlopen(base_url + file_name) as response, open(out_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

    def read_relevant_files(self):
        for suffix in Data.get_suffixes():
            yield self.read_data_from_zip(suffix)

    def read_data_from_zip(self, suffix):
        file_name = 'factorio-data-' + self.version_number + '.zip'
        with ZipFile(Data.data_folder_path / file_name, 'r') as my_zip:
            folder_name = my_zip.filelist[0].filename
            try:
                text_stream = my_zip.read(folder_name + suffix)
                return text_stream
            except FileNotFoundError as e:
                raise e

    # todo recipe data parser - parse data from lua into base classes, maybe have classes handle it themselves
    @staticmethod
    def data_extender(text_stream):
        check_text =b'data:extend(\n{', b'data:extend\n{'
        text_stream = text_stream.lstrip()
        for txt in check_text:
            if not text_stream.startswith(txt):  # some files do not start with check text
                #this doesnt handle capsule.lua
                # print('not data file')
                continue
            text_stream = text_stream.partition(txt)[2]
            for data_line in text_stream.split(b'\n  {\n    '):
                if data_line != b'' and data_line.startswith(b'type = "recipe"'):
                    dl = data_line.partition(b'type = "recipe",')[2]
                    yield dl
            break
                # print(dl)
        # for recipe in Recipe.recipes_list:
        #     print(recipe)
        # for v in Item.items_dict.values():
        #     print(v)

    # https://note.nkmk.me/en/python-check-int-float/
    @staticmethod
    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()

    # https://stackoverflow.com/questions/645312/what-is-the-quickest-way-to-http-get-in-python/54856660#54856660
    @staticmethod
    def get_latest_version():
        try:
            http = PoolManager()
            r = http.request('GET', 'https://raw.githubusercontent.com/wube/factorio-data/master/base/info.json')
            line = r.data.decode('utf-8').split('  "version": "')[1]
            current_version = line.split('"')[0]
            return current_version
        except MaxRetryError:
            # todo handle this error by searching files to get latest version
            return '1.0.0'

    @staticmethod
    def get_all_versions():
        versions = list()
        versions.append(Data.get_latest_version())

        file_path = Data.data_folder_path / 'versions.txt'
        try:
            with open(file_path, 'r') as file:
                # if current version matches the latest version saved in file
                if versions[0] == file.readline().rstrip('\n'):
                    while versions[-1] != '0.5.0':  # earliest version released
                        versions.append(file.readline().rstrip('\n'))
        except FileNotFoundError as e:
            # todo manage this error
            print(f"Oopsies: {e}")
            pass

        url = 'https://github.com/wube/factorio-data/releases'
        split_string = '<a href="/wube/factorio-data/releases/tag/'

        # this should only run if the current version does not show up in the file

        # todo instead of getting all files every time, just append the missing ones to the start of the file
        # todo this takes a long time with only 10 versions per page. There is a way to get 100.
        while versions[-1] != '0.5.0':  # earliest version released
            http = PoolManager()
            r = http.request('GET', url)
            for line in r.data.decode('utf-8').split(split_string):
                if Data.is_integer(line[0]):  # an unwanted string may get through
                    versions.append(line.split('"')[0])
            url = 'https://github.com/wube/factorio-data/releases?after=' + versions[-1]

        return versions

    @staticmethod
    def write_versions(versions):
        file_path = Data.data_folder_path / 'versions.txt'
        with open(file_path, 'w+') as file:
            for version in versions:
                file.write(version + '\n')

    @classmethod
    def get_suffixes(cls):
        for suffix in cls.suffixes:
            s = suffix
            suffix = f'base/prototypes/recipe/{s}.lua'
            yield str(suffix)
        return StopIteration


# print(*Data.get_all_versions(), sep='\n')
# d = Data('1.0.0')



