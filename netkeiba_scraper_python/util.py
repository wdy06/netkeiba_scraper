import pathlib
import re


def load_url_list(file_path):
    with open(file_path, 'r') as f:
        url_list = []
        for line in f.readlines():
            url_list.append(line.rstrip('\n'))
        return url_list


def load_html_file_list(dir_path):
    dir_path = pathlib.Path(dir_path)
    html_list = list(dir_path.glob('*'))
    html_list = ['file://' + str(filename.resolve()) for filename in html_list]
    return html_list


def jockey_profile_url2id(text):
    # http://db.netkeiba.com/jockey/profile/XXXXX/
    text = re.sub('(http://db.netkeiba.com/jockey/profile/)', '', text)
    return text.replace('/', '')


def horse_profile_url2id(text):
    # http://db.netkeiba.com/horse/XXXXXXXXXX/
    text = re.sub('(http://db.netkeiba.com/horse/)', '', text)
    return text.replace('/', '')


def race_url2id(text):
    text = re.sub('(http://db.netkeiba.com/race/)', '', text)
    return text.replace('/', '')
