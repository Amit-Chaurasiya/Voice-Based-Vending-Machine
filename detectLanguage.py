import googletrans
import speech_recognition as sr
import gtts
import playsound

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak....")
    voice = recognizer.listen(source,phrase_time_limit=30)
    # text = recognizer.recognize_google(voice)
    text = recognizer.recognize_bing(voice,)
    print(text)


translator = googletrans.Translator()
translation = translator.translate(text, dest='mr')
print(translation)

# converted_audio = gtts.gTTS(translation, lang='mr')
# converted_audio.save("hello.mp3")
# playsound.playsound("hello.mp3")