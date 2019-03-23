"""
    Download and convert youtube videos to mp3 files. Because online is too slow.
"""

import os

from pathlib import Path
from pytube import YouTube


DIRECTORY = Path("./data/music")
URLS_FILE = Path("video_urls")


def get_from_file(url_list):
    print()
    print(os.getcwd())
    with open(URLS_FILE, "r") as urls:
        for url in urls:
            if not url.startswith("http") and not url.startswith("www"):
                url = "http://www.youtube.com/watch?v={}".format(url)
            url = url.strip()
            if url is not "":
                url_list.append(url)


def get_from_input(url_list):
    url = input("> ")
    while url != "":
        if not url.startswith("http") and not url.startswith("www"):
            url = "http://www.youtube.com/watch?v={}".format(url)
        url = url.strip()
        url_list.append(url)
        url = input("> ")


os.chdir(DIRECTORY)

vids = []
try:
    get_from_file(vids)
except Exception as e:
    print(e)
if len(vids) == 0:
    get_from_input(vids)

for video_url in vids:
    print("Downloading video from {}".format(video_url))
    try:
        video = YouTube(video_url)
        audio_stream = video.streams.filter(only_audio=True).first()
        if audio_stream:
            audio_stream.download()
        else:
            video.streams.first().download()
    except Exception as e:
        print("Download failed:", e)
        try:
            video = YouTube(video_url)
            audio_stream = video.streams.filter(only_audio=True).first()
            if audio_stream:
                audio_stream.download()
            else:
                video.streams.first().download()
        except Exception as er:
            print(er)
            print("Failed to download {}".format(video_url))


print("Download complete")
