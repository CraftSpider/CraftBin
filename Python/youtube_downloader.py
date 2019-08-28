"""
    Download and convert youtube videos to mp3 files. Because online is too slow.
"""

import os
import pathlib
import subprocess

from pytube import YouTube


DIRECTORY = pathlib.Path("./data/music")
URLS_FILE = pathlib.Path("video_urls")


def get_from_file(url_list):
    with open(URLS_FILE, "r") as urls:
        for url in urls:
            if not url.startswith("http") and not url.startswith("www"):
                url = f"http://www.youtube.com/watch?v={url}"
            url = url.strip()
            if url != "":
                url_list.append(url)


def get_from_input(url_list):
    url = input("> ")
    while url != "":
        if not url.startswith("http") and not url.startswith("www"):
            url = f"http://www.youtube.com/watch?v={url}"
        url = url.strip()
        url_list.append(url)
        url = input("> ")


def try_download(video, times=2):
    audio_stream = video.streams.filter(only_audio=True).first()
    if audio_stream is None:
        audio_stream = video.streams.first()

    while times > 0:
        try:
            audio_stream.download()
            return audio_stream.default_filename
        except Exception as e:
            print(f"Download failed: {e.__class__.__name__} {e}")
            times -= 1

    print(f"Failed to download {video.watch_url}")
    return None


def main():
    os.chdir(DIRECTORY)
    urls = []
    try:
        get_from_file(urls)
    except Exception as e:
        print(e)
    if len(urls) == 0:
        get_from_input(urls)

    print("Prefetching all videos")
    videos = [YouTube(x) for x in urls]

    filenames = []
    for video in videos:
        print(f"Downloading video \"{video.title}\" from {video.watch_url}")
        filenames.append(try_download(video))

    for filename in filenames:
        if filename is None:
            continue
        newname = ".".join(filename.split(".")[:-1]) + ".mp3"
        subprocess.call(["ffmpeg", "-i", filename, newname])

    print("Download complete")


if __name__ == "__main__":
    main()
