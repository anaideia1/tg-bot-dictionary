# data for PURPOSE stage
REASONS = [
    'Just for fun',
    'To give 20 points for lab',
    'For faire usage as a dictionary',
    'Testing...',
]

REASONS_ANSWERS = {
    'Just for fun': 'Well, without further interruptions lets begin!',
    'To give 20 points for lab': 'It\'s pretty gallantly and kindly.',
    'For faire usage as a dictionary': 'OK, you are welcome.',
    'Testing...': 'My lllooord o_0, our humble servant to your service!',
}


# data for TARGET_LANGUAGE stage
LANGUAGES = [
    'English',
    'French',
    'German',
    'Ukrainian',
    'Spanish',
]

LANGUAGE_CODES = {
    'English': 'en-US',
    'French': 'fr-FR',
    'German': 'de-DE',
    'Ukrainian': 'uk-UA',
    'Spanish': 'es-ES',
}


# data for DISHES stage
ENGLISH_DISHES = [
    'Yorkshire Pudding',
    'Fish and Chips',
    'English Pancakes',
    'Shepherd\'s Pie',
    'Black Pudding',
]

FRENCH_DISHES = [
    'Chanterelle Omelets',
    'Ratatouille',
    'Bouillabaisse',
    'Crêpes',
    'Crème Brûlée',
]

GERMAN_DISHES = [
    'Beer',
    'Sausages',
    'Döner kebab',
    'Schnitzel',
    'Currywurst',
]

UKRAINIAN_DISHES = [
    'Borshch',
    'Varenyky',
    'Holubtsi',
    'Banosh',
    'Syrnyky',
]

SPANISH_DISHES = [
    'Paella Valenciana',
    'Gazpacho',
    'Jamón',
    'Tortilla',
    'Churros',
]

NATION_DISHES = {
    'English': ENGLISH_DISHES,
    'French': FRENCH_DISHES,
    'German': GERMAN_DISHES,
    'Ukrainian': GERMAN_DISHES,
    'Spanish': SPANISH_DISHES,
}


# voice gender

VOICES = [
    'Male',
    'Female',
    'Neutral',
]

from google.cloud import texttospeech
VOICES_CODES = {
    'Male': texttospeech.SsmlVoiceGender.MALE,
    'Female': texttospeech.SsmlVoiceGender.FEMALE,
    'Neutral': texttospeech.SsmlVoiceGender.NEUTRAL,
}