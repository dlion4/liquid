import os
import boto3
from pathlib import Path
from yt_dlp import YoutubeDL
from django.conf import settings


# Your AWS credentials
AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
AWS_S3_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

# Path to save the downloaded files locally before uploading to S3
APPS_DIR = Path(__file__).resolve(strict=True).parent.parent
YOUTUBE_DOWNLOAD_DIR = os.path.join(APPS_DIR, "media", "audio", "youtube")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def download_youtube_from_video_url(url):
    videoinfo = YoutubeDL().extract_info(url=url, download=False)
    length = videoinfo['duration']
    filename = f"{YOUTUBE_DOWNLOAD_DIR}{videoinfo['id']}.mp3"
    s3_filename = f"audio/youtube/{videoinfo['id']}.mp3"

    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }

    with YoutubeDL(options) as ydl:
        ydl.download([videoinfo['webpage_url']])

    # Upload to S3
    s3_client.upload_file(filename, AWS_S3_BUCKET_NAME, s3_filename)

    # Generate S3 URL
    s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{s3_filename}"

    # Clean up the local file
    os.remove(filename)

    return s3_url, length

# Testing by running this file
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=q_eMJiOPZMU"
    filename, length = download_youtube_from_video_url(url)
    print(f"Audio file: {filename} with length {length} seconds")
    print("Done!")
