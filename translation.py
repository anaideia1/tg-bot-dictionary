import six

from typing import Tuple

from google.cloud import translate_v2 as translate
from google.oauth2.credentials import Credentials


class GCPTranslation:
    def __init__(self, creds: Credentials) -> None:
        """
        Initialize GCP Translation client with credentials
        :param creds: Credentials for GCP TextToSpeech client
        :return: None
        """
        self.client = translate.Client(credentials=creds)

    def translate(self, text: str, target: str) -> Tuple[str, str, str]:
        """
        Translate source text to target language
        :param text: source text on any language
        :param target: target language on which we should translate
        :return: tuple of translated text, source text and source language
        """
        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        result = self.client.translate(text, target_language=target)

        translated_text = result['translatedText']
        input_text = result['input']
        source_language = result['detectedSourceLanguage']
        print(f'Text: {input_text}')
        print(f'Translation: {translated_text}')
        print(f'Detected source language: {source_language}')

        return translated_text, input_text, source_language
