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

class DeepgramAudioTranscription():
    deepgram:DeepgramClient
    filename:str
    api_key:str = DEEPGRAM_API_KEY

    @property
    def _prepare_deepgram(self)->DeepgramClient:
        self.deepgram = DeepgramClient('', ClientOptionsFromEnv(
            api_key=self.api_key
        ))
        return self.deepgram
        

    @property
    def _prepare_file_location(self)->tuple[str, str]:
        instance_file_name = generate_random_file_name(12)
        # Ensure the directory exists
        if not os.path.exists(TRANSCRIPT_DOWNLOAD_DIR):
            os.makedirs(TRANSCRIPT_DOWNLOAD_DIR)

        # Path for the local file
        local_file_path = os.path.join(TRANSCRIPT_DOWNLOAD_DIR, f"{instance_file_name}.txt")
        s3_transcript_filename = f"transcripts/files/{instance_file_name}.txt"

        return local_file_path, s3_transcript_filename
    

    
    def _save_transcript_to_aws3_cloud_location(self, transcript:str)->str:
        local_file_path, s3_transcript_filename = self._prepare_file_location
        
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

        return s3_url

    def transcribe_audio(self, filename, limit=8):
    
        AUDIO_URL = {
            "url": f"{filename}"
        }
        try:
            # STEP 2 Call the transcribe_url method on the prerecorded class
            options: PrerecordedOptions = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
                topics=True, 
                language="en",

            )
            response = self._prepare_deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)
            # print(f"response: {response}\n\n")
            # print(f"metadata: {response['metadata']}\n\n")
            transcript = response.results.channels[0].alternatives[0]['transcript']
            topic = response.results.topics.segments[0]['text']
            theme = response.results.topics.segments[0]['topics'][0]['topic']

            # print(transcript)

            s3_url = self._save_transcript_to_aws3_cloud_location(transcript)

            return s3_url, transcript, theme

        except Exception as e:
            # print(f"Exception: {e}")
            print("Error from the deep gram endpoint", e)
            return str(e), f"Something went wrong. Please try again {e}", str(e)






