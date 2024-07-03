import os
from deepgram import (
    DeepgramClient,
    ClientOptionsFromEnv,
    PrerecordedOptions,
)
import os
import random
import string

DEEPGRAM_API_KEY = os.environ.get('DEEPGRAM_API_KEY')
from .download import s3_client, AWS_S3_BUCKET_NAME, APPS_DIR
TRANSCRIPT_DOWNLOAD_DIR = os.path.join(APPS_DIR, "media", "transcripts", "files")

def generate_random_file_name(limit=8):
    return "".join(random.choices(string.ascii_letters, k=limit))

def transcribe_audio(filename, limit=8):
    deepgram: DeepgramClient = DeepgramClient('', ClientOptionsFromEnv(
        api_key=DEEPGRAM_API_KEY
    ))

    instance_file_name = generate_random_file_name(limit)

        # Ensure the directory exists
    if not os.path.exists(TRANSCRIPT_DOWNLOAD_DIR):
        os.makedirs(TRANSCRIPT_DOWNLOAD_DIR)

    # Path for the local file
    local_file_path = os.path.join(TRANSCRIPT_DOWNLOAD_DIR, f"{instance_file_name}.txt")
    s3_transcript_filename = f"transcripts/files/{instance_file_name}.txt"

    print(TRANSCRIPT_DOWNLOAD_DIR)
    print(local_file_path)
    print(s3_transcript_filename)


    AUDIO_URL = {
        "url": f"{filename}"
    }
    try:
        # STEP 2 Call the transcribe_url method on the prerecorded class
        options: PrerecordedOptions = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )
        response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)
        # print(f"response: {response}\n\n")
        # print(f"metadata: {response['metadata']}\n\n")
        transcript = response.results.channels[0].alternatives[0]['transcript']

        # print(transcript)

        # Write the transcript to a local file
        with open(local_file_path, "w") as f:
            f.write(transcript)

        # Upload to S3
        s3_client.upload_file(local_file_path, AWS_S3_BUCKET_NAME, s3_transcript_filename)
        # print(transcript)
        # Generate S3 URL
        s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{s3_transcript_filename}"

        # Clean up the local file
        try:
            os.remove(local_file_path)
            print(f"Local file deleted: {local_file_path}")

        except OSError as e:

            print(f"Error deleting local file: {e}")
            print(e)
            raise

        return s3_url, transcript

    except Exception as e:
        # print(f"Exception: {e}")
        print("Error from the deep gram endpoint", e)
        return str(e), f"Something went wrong. Please try again {e}"





# Upload to S3
# try:
#     s3_client.upload_file(local_file_path, AWS_S3_BUCKET_NAME, s3_transcript_filename)
#     print(f"File uploaded to S3: {s3_transcript_filename}")
# except boto3.exceptions.S3UploadFailedError as e:
#     print(f"Failed to upload file to S3: {e}")
#     raise

# # Generate S3 URL
# s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{s3_transcript_filename}"
# print(f"S3 URL: {s3_url}")

# # Clean up the local file
# try:
#     os.remove(local_file_path)
#     print(f"Local file deleted: {local_file_path}")
# except OSError as e:
#     print(f"Error deleting local file: {e}")
#     raise