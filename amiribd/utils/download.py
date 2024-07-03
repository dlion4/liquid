import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pathlib import Path

APPS_DIR = Path(__file__).resolve(strict=True).parent.parent

YOUTUBE_DOWNLOAD_DIR = os.path.join(APPS_DIR , "media" , "audio" , "youtube")

from yt_dlp import YoutubeDL



def download_youtube_from_video_url(url):
    videoinfo = YoutubeDL().extract_info(url=url, download=False)
    length = videoinfo['duration']
    filename = f"{YOUTUBE_DOWNLOAD_DIR}{videoinfo['id']}.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }
    with YoutubeDL(options) as ydl:
        ydl.download([videoinfo['webpage_url']])
    return filename, length


# Testing by running this file
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=q_eMJiOPZMU"
    filename, length = download_youtube_from_video_url(url)
    print(f"Audio file: {filename} with length {length} seconds")
    print("Done!")
