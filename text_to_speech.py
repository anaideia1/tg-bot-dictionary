import os.path
from google.cloud import texttospeech
from google.oauth2.credentials import Credentials


class GCPTextToSpeech:
    def __init__(self, creds: Credentials) -> None:
        """
        Initialize GCP TextToSpeech client with credentials
        :param creds: Credentials for GCP TextToSpeech client
        :return: None
        """
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient(credentials=creds)

    def set_speech_params(
            self, lang: str = 'en-US',
            voice: int = texttospeech.SsmlVoiceGender.NEUTRAL,
    ) -> None:
        """
        Set few params for voice in audio
        :param lang: Language code for text-to-speech voice
        :param voice: Voice specification for text-to-speech voice
        :return: None
        """
        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        self.voice = texttospeech.VoiceSelectionParams(
            language_code=lang,
            ssml_gender=voice
        )

        # Select the type of audio file you want returned
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def text_to_speech(self, text: str, lang: str,
                       voice: int = texttospeech.SsmlVoiceGender.NEUTRAL,):
        """
        Return audio with voiceover of particular text on some language
        :param text: text for transformation
        :param lang: Language code for text-to-speech voice
        :param voice: Voice specification for text-to-speech voice
        :return: audio_content from response on GCP client.synthesize_speech
        """
        # Set the text input to be synthesized
        self.synthesis_input = texttospeech.SynthesisInput(text=text)

        self.set_speech_params(lang=lang, voice=voice)
        return self.get_audio()

    def get_audio(self):
        """
        Get audio from GCP TextToSpeech client response
        :return: audio_content from response on GCP client.synthesize_speech
        """
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=self.synthesis_input,
            voice=self.voice,
            audio_config=self.audio_config
        )
        return response.audio_content

    def text_to_speech_in_mp3_file(self, text: str, lang: str) -> None:
        """
        Create file with audio voiceover of particular text on some language
        :param text: text for transformation
        :param lang: Language code for text-to-speech voice
        :return: None
        """
        # The response's audio_content is binary.
        audio_content = self.text_to_speech(text, lang)

        dir_path = os.path.dirname(__file__)
        output_file = os.path.join(dir_path, 'output.mp3')
        with open(output_file, "wb") as out:
            # Write the response to the output file.
            out.write(audio_content)
            print('Audio content written to file "output.mp3"')
