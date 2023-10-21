from translate import Translator
from gtts import gTTS
import pygame
import os
import random


# Function to translate a text to Hindi and play it as audio
def translate_and_play_audio(text, language):
    try:
        # Translate the text to Hindi
        translator = Translator(to_lang=language)
        translation = translator.translate(text)

        # Print the translated text
        print("Translated Text (Hindi):", translation)

        # Convert the translated text to speech in Hindi
        tts = gTTS(text=translation, lang=language)

        # Save the audio to a temporary file
        audio_file = "translated_audio.mp3"
        tts.save(audio_file)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load and play the audio
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Clean up: remove the temporary audio file
        os.remove(audio_file)

    except Exception as e:
        print("Translation or audio conversion error:", e)


# Input text to be translated and played in Hindi
# input_text = "Lights on, snacks ready. Let's get started!"
thanks_messages = [
    "Coins or UPI? The choice is yours for a tasty treat!",
    "Insert coins or make a quick UPI payment to satisfy your cravings.",
    "Cash or cashless? We accept both coins and UPI payments.",
    "Coins jingling or UPI ready? Pick your preferred payment method.",
    "Cash in coins or go digital with UPI for a seamless snack experience.",
    "Pay with the jingle of coins or the tap of your UPI app.",
    "Coins or UPI scan? You're just a payment away from your snack.",
    "Coins or UPI - either way, your snack is just moments away!",
    "Cash or digital, we've got you covered: coins or UPI payment.",
    "Choose your payment adventure: coins clinking or UPI beeping!",
    "Coins or UPI, we make snacking easy and convenient!",
    "Tap into the future with UPI or keep it classic with coins.",
    "From coins to UPI, we've got your payment preferences covered.",
    "Your snack, your way – whether with coins or a UPI transaction.",
    "Coins or UPI, the choice is yours, and the snack is ready to go!"
]

random_message = random.choice(thanks_messages)
# Translate and play the text in Hindi
translate_and_play_audio(random_message,"ml")

# Quit pygame when done
pygame.quit()
