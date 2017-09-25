"""
Download count for github releases.

Uses the github REST API
https://developer.github.com/v3/
https://developer.github.com/v3/repos/releases/#get-a-single-release

With JSON information from
https://api.github.com/repos/sys-bio/tellurium/releases
"""
from __future__ import print_function, absolute_import
import requests
import json
import pprint
import pandas as pd

from matplotlib import pyplot as plt

TELLURIUM_GIT_URL ="https://api.github.com/repos/sys-bio/tellurium/releases"


def get_git_releases_json(url, params={}):
    """ Gets the JSON release information from github. """
    response = requests.get(url=url, params=params)
    data = json.loads(response.text)
    # pprint.pprint(data)
    return data

def parse_release_json(data):
    """ Parses the release JSON data in pandas data frame."""
    info = {}
    rows = []
    for release in data:
        print(release)

        info = {}
        for field in ['tag_name', 'published_at']:
            info[field] = release[field]

        download_count = 0
        for asset in release['assets']:
            # sum over mac, win, linux for release
            download_count += asset['download_count']
        info['download_count'] = download_count

        rows.append(info)

    # dataframe which is sorted by publishing dates
    df = pd.DataFrame(rows)
    df = df.sort_values(['published_at'])

    # calculate cumsum of downloads
    df['download_cum'] = df['download_count'].cumsum()

    # sort back
    df = df.sort_values(['published_at'], ascending=False)

    # parse times
    df['published_at'] = pd.to_datetime(df.published_at)

    return df

def plot_release_df(df):
    """ Creates plot of the downloads.

    :param df:
    :return:
    """
    fig, ax = plt.subplots()
    ax.plot(df.published_at, df.download_count, linestyle="-", marker="o", linewidth=2, label="Downloads", color="darkgreen")
    ax.plot(df.published_at, df.download_cum, linestyle="-", marker="o", linewidth=2, label="Cumulative Downloads",
             color="blue")
    for i, txt in enumerate(df.tag_name):
        ax.annotate(txt, (df.published_at[i], df.download_count[i]+10))

    ax.set_title("Tellurium GitHub Downloads")
    ax.set_xlabel("Release Date")
    ax.set_ylabel("Downloads")

    ax.legend()
    plt.savefig("tellurium_github_downloads.png")


if __name__ == "__main__":
    json = get_git_releases_json(TELLURIUM_GIT_URL)
    df = parse_release_json(json)
    print(df)
    plot_release_df(df)
