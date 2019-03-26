"""
    Download and convert youtube videos to mp3 files. Because online is too slow.
"""

import os
import pathlib

from pytube import YouTube


DIRECTORY = pathlib.Path("./data/music")
URLS_FILE = pathlib.Path("video_urls")


def get_from_file(url_list):
    with open(URLS_FILE, "r") as urls:
        for url in urls:
            if not url.startswith("http") and not url.startswith("www"):
                url = f"http://www.youtube.com/watch?v={url}"
            url = url.strip()
            if url is not "":
                url_list.append(url)


def get_from_input(url_list):
    url = input("> ")
    while url != "":
        if not url.startswith("http") and not url.startswith("www"):
            url = f"http://www.youtube.com/watch?v={url}"
        url = url.strip()
        url_list.append(url)
        url = input("> ")


def try_download(url, times=2):
    video = YouTube(url)
    audio_stream = video.streams.filter(only_audio=True).first()
    if audio_stream is None:
        audio_stream = video.streams.first()

    while times > 0:
        try:
            audio_stream.download()
            return
        except Exception as e:
            print("Download failed:", e)
            times -= 1

    print(f"Failed to download {url}")


def main():
    os.chdir(DIRECTORY)
    vids = []
    try:
        get_from_file(vids)
    except Exception as e:
        print(e)
    if len(vids) == 0:
        get_from_input(vids)

    for video_url in vids:
        print(f"Downloading video from {video_url}")
        try_download(video_url)

    print("Download complete")


if __name__ == "__main__":
    main()
