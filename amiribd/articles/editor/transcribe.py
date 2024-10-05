import os
import random
import string
from pathlib import Path

from deepgram import ClientOptionsFromEnv
from deepgram import DeepgramClient
from deepgram import PrerecordedOptions

from .download import APPS_DIR
from .download import AWS_S3_BUCKET_NAME
from .download import s3_client

DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")


TRANSCRIPT_DOWNLOAD_DIR = Path(APPS_DIR/"media"/"transcripts"/ "files")

def generate_random_file_name(limit=8):
    return "".join(random.choices(string.ascii_letters, k=limit))

class DeepgramAudioTranscription:
    deepgram:DeepgramClient
    filename:str
    api_key:str = DEEPGRAM_API_KEY

    @property
    def _prepare_deepgram(self)->DeepgramClient:
        self.deepgram = DeepgramClient("", ClientOptionsFromEnv(
            api_key=self.api_key,
        ))
        return self.deepgram


    @property
    def _prepare_file_location(self)->tuple[str, str]:
        instance_file_name = generate_random_file_name(12)
        # Ensure the directory exists
        if not os.path.exists(TRANSCRIPT_DOWNLOAD_DIR):  # noqa: PTH110
            os.makedirs(TRANSCRIPT_DOWNLOAD_DIR)  # noqa: PTH103

        # Path for the local file
        local_file_path = os.path.join(  # noqa: PTH118
            TRANSCRIPT_DOWNLOAD_DIR, f"{instance_file_name}.txt")
        s3_transcript_filename = f"transcripts/files/{instance_file_name}.txt"

        return local_file_path, s3_transcript_filename

    def _save_transcript_to_aws3_cloud_location(self, transcript:str)->str:
        local_file_path, s3_transcript_filename = self._prepare_file_location
        # Write the transcript to a local file
        with Path.open(local_file_path, "w") as f:
            f.write(transcript)

        # Upload to S3
        s3_client.upload_file(local_file_path, AWS_S3_BUCKET_NAME, s3_transcript_filename)
        # Generate S3 URL
        s3_url = f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{s3_transcript_filename}"

        # Clean up the local file
        try:
            Path.unlink(local_file_path)
        except OSError:
            """"""
        return s3_url

    def transcribe_audio(self, filename, limit=8):
        audio_url = {"url": f"{filename}"}
        try:
            # STEP 2 Call the transcribe_url method on the prerecorded class
            options: PrerecordedOptions = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
                topics=True,
                language="en",

            )
            response = self._prepare_deepgram.listen.prerecorded.v(
                "1").transcribe_url(audio_url, options)
            transcript = response.results.channels[0].alternatives[0]["transcript"]
            topic = response.results.topics.segments[0]["text"]  # noqa: F841
            theme = response.results.topics.segments[0]["topics"][0]["topic"]
            s3_url = self._save_transcript_to_aws3_cloud_location(transcript)
            return s3_url, transcript, theme  # noqa: TRY300

        except Exception as e:  # noqa: BLE001
            return str(e), f"Something went wrong. Please try again {e}", str(e)






