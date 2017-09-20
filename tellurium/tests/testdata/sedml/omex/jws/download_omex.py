"""
Downloads latest JWS simulation descriptions.

Necessary to update the script with changing JWS webpage.
"""
import os
import requests
from bs4 import BeautifulSoup
import pprint
import shutil

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
NUM_PAGES = 4
URL = "http://jjj.mib.ac.uk/models/experiments/?&page={}"
OMEX_DIR = os.path.join(THIS_DIR, 'omex')


def jws_omex_dict():
    """ Returns dictionary of available JWS combine archives.

    :return: { id: download_url } dict
    """
    jws_omex = {}
    num_omex = 0
    for page_iter in range(NUM_PAGES):
        url = URL.format(page_iter+1)  # 1 based counting
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')

            # select all <a> in <td>
            items = soup.select('td a')
            # only interested in the download links
            links = [a.get("href") for a in items if "combinearchive?download=1" in a.get('href')]
            print("N(page={}) = {}".format(page_iter+1, len(links)))
            num_omex += len(links)
            for url in links:
                tokens = url.split('/')
                name = tokens[3]
                jws_omex[name] = "http://jjj.mib.ac.uk" + url

    # pprint.pprint(jws_omex)
    print('---------')
    print(num_omex)
    return jws_omex


def download_omex(url, omex_path):
    """ Download url to omex_path.

    :param url:
    :param omex_path:
    :return:
    """
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(omex_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def download_jws_omex():
    jws_dict = jws_omex_dict()
    num_omex = len(jws_dict)
    count = 1
    for sid, url in jws_dict.items():
        omex_path = os.path.join(OMEX_DIR, "{}.sedx".format(sid))
        if os.path.exists(omex_path):
            os.remove(omex_path)
        print(count, '/', num_omex, ':', url, '-->', omex_path)
        download_omex(url=url, omex_path=omex_path)
        count += 1


if __name__ == "__main__":
    download_jws_omex()
