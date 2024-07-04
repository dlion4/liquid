from deepgram import (
    DeepgramClient,
    ClientOptionsFromEnv,
    PrerecordedOptions,
)

DEEPGRAM_API_KEY = "df843830a8d37260efce96a1134363b34cef5188"

AUDIO_URL = {
    "url": "https://earnkraft.s3.eu-north-1.amazonaws.com/audio/youtube/Ko52pn1KXS0.mp3"
}

def main():
    try:
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        options = PrerecordedOptions(
            model="nova-2",
            language="en",
            topics=True, 
            smart_format=True, 
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)
        topic = response.results.topics.segments[0]['text']
        theme = response.results.topics.segments[0]['topics'][0]['topic']

        print("topic: ", topic)
        print("theme: ", theme)

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()