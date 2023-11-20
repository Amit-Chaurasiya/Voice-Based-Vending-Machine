import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime, timedelta
import random
from googletrans import Translator
import tkinter as tk
from PIL import Image, ImageTk
import qrcode
import os
import threading
import secrets
import openpyxl

TRANSACTION_CODE_FILE = "/home/siesgst/Desktop/Vending Machine/transaction_codes.txt"


def generate_transaction_code():
    return secrets.token_hex(16)  # Generates a random 32-character hexadecimal code


def save_transaction_code(code, product, amt):
    with open(TRANSACTION_CODE_FILE, "a") as file:
        file.write(f"{code}\t{product}\t{amt}\n")


def is_transaction_code_unique(code):
    with open(TRANSACTION_CODE_FILE, "r") as file:
        existing_codes = file.read().splitlines()
    return code not in existing_codes


def generate_transaction_code():
    return secrets.token_hex(16)


L1 = 25
L2 = 8
L3 = 7
L4 = 1

C1 = 12
C2 = 16
C3 = 20
C4 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def say(text, language):
    try:
        # Translate the text to the target language
        translator = Translator()
        translation = translator.translate(text, dest=language)

        # Print the translated text
        print("Text: ", translation.text)

        # Convert the translated text to speech in the target language
        tts = gTTS(text=translation.text, lang=language)

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
        import os
        os.remove(audio_file)

    except Exception as e:
        print("Translation or audio conversion error:", e)



def readKeypad(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        return characters[0]
    if GPIO.input(C2) == 1:
        return characters[1]
    if GPIO.input(C3) == 1:
        return characters[2]
    if GPIO.input(C4) == 1:
        return characters[3]
    GPIO.output(line, GPIO.LOW)


def selectInputMethod():
    say("How would you like to vend your product? Two options - by voice or by manual selection. Press star to use keypad or press # to use voice for further process", "en")
    while True:
        if readKeypad(L4, ["*", "0", "#", "D"]) == "*":
            say("Thank you for selecting Keypad", "en")
            return "Manual"
        elif readKeypad(L4, ["*", "0", "#", "D"]) == "#":
            say("Thank you for selecting Voice", "en")
            return "voice"


def selectLanguageKeypad():
    say("Please Select one language.", "en")
    say("Press A for Hindi", "hi")
    say("B for Marathi", "mr")
    say("C for English", "en")
    say("D for Malayalam", "ml")
    while True:
        # call the readKeypad function for each row of the keypad
        if readKeypad(L1, ["1", "2", "3", "A"]) == "A":
            say("Thankyou for selecting Hindi", "hi")
            return "hi"
        elif readKeypad(L2, ["4", "5", "6", "B"]) == "B":
            say("Thankyou for selecting Marathi", "mr")
            return "mr"
        elif readKeypad(L3, ["7", "8", "9", "C"]) == "C":
            say("Thankyou for selecting English", "en")
            return "en"
        elif readKeypad(L4, ["*", "0", "#", "D"]) == "D":
            say("Thankyou for selecting Malayalam", "ml")
            return "ml"
        time.sleep(0.5)


def selectLanguageVoice():
    say("Please Select one language. ", "en")
    say("say hindee,", "hi")
    say("Say Marathi,", "mr")
    say("Say English,", "en")
    say("Say Malayalam.", "ml")
    while True:
        language = recognize_speech()
        if str(language).lower() == "hindi":
            say("Thankyou for selecting Hindi", "hi")
            return "hi"
        elif str(language).lower() == "marathi":
            say("Thankyou for selecting Marathi", "mr")
            return "mr"
        elif str(language).lower() == "english":
            say("Thankyou for selecting English", "en")
            return "en"
        elif str(language).lower() == "malayalam":
            say("Thankyou for selecting Malayalam", "ml")
            return "ml"
        time.sleep(0.5)


def welcomeMessages():
    vending_messages = [
        "Welcome to the vending experience.",
        "Hello, what do you want to eat today?",
        "What are you looking forward to eating",
        "Ready to serve you. What will you eat today?",
        "Welcome to snacks Central please select your product"
    ]

    random_message = random.choice(vending_messages)
    return random_message


def availableProducts():
    availableproductsmessages = [
        "ek chunen: kaidabaree, kitakait, kurakure, ya lays."
    ]

    random_message = random.choice(availableproductsmessages)
    return random_message


def selectProductKeypad():
    say("krpaya aap jo chaahate hain use chunen, kaidabaree ke lie 1 dabaen, kitakait ke lie 2 dabaen, kurakure ke lie 3 dabaen, lays ke lie 4 dabaen",
        lang)
    while True:
        # call the readKeypad function for each row of the keypad
        if readKeypad(L1, ["1", "2", "3", "A"]) == "1":
            say("aapane kaidabaree ko chuna", lang)
            return "cadbury"
        elif readKeypad(L1, ["1", "2", "3", "A"]) == "2":
            say("aapane kitakait ko chuna", lang)
            return "kitkat"
        elif readKeypad(L1, ["1", "2", "3", "A"]) == "3":
            say("aapane kurakure ko chuna", lang)
            return "kurkure"
        elif readKeypad(L2, ["4", "5", "6", "B"]) == "4":
            say("aapane lez ko chuna", lang)
            return "lays"
        elif readKeypad(L4, ["*", "0", "#", "D"]) == "0":
            say("vending masheen band ho rahee hai", lang)
            return "keep quiet"
        time.sleep(0.5)


def paymentMethodOptions():
    payment_options = [
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
        "Your snack, your way, whether with coins or a UPI transaction.",
        "Coins or UPI, the choice is yours, and the snack is ready to go!"
    ]

    random_message = random.choice(payment_options)
    return random_message


def thankYouMessages():
    thanks_messages = [
        "Thank you for choosing us for your snack break!",
        "Your satisfaction is our delight. Thanks for shopping with us!",
        "A big 'thank you' for making us your snack destination!",
        "We are grateful for your purchase. Enjoy your treats!",
        "Thanks for being a part of our vending machine family.",
        "Your choice makes us smile. Thanks for shopping with us!",
        "Your snack adventure starts here. Thanks for choosing us!",
        "We are delighted you stopped by. Thanks for shopping!",
        "Your support means the world to us. Thank you for your purchase!",
        "As your snacks are dispensed, our gratitude is also delivered. Thank you!",
        "We are vending happiness, and you've made our day. Thank you!",
        "Your choice makes us vending happy. Thanks for your patronage!"
    ]

    random_message = random.choice(thanks_messages)
    return random_message


def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        recognized_text = recognizer.recognize_google(audio)
        print("You said:", recognized_text)
        return recognized_text

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return None
    except sr.ALSAError:
        print("ALSA error: There was a problem with the audio device.")
        return None


def dairyMilk():
    servo_pin = 2
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(0)
    try:
        for _ in range(1):
            pwm.ChangeDutyCycle(12)  # 0 degrees
            time.sleep(0.1)
            pwm.ChangeDutyCycle(7.5)  # 90 degrees (neutral position)
            time.sleep(0.1)
            pwm.ChangeDutyCycle(12.5)  # 180 degrees
            time.sleep(0.1)
    finally:
        pwm.stop()


def Kitkat():
    servo_pin = 3
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(0)
    try:
        for _ in range(1):
            pwm.ChangeDutyCycle(12)  # 0 degrees
            time.sleep(0.1)
            pwm.ChangeDutyCycle(7.5)  # 90 degrees (neutral position)
            time.sleep(0.1)
            pwm.ChangeDutyCycle(12.5)  # 180 degrees
            time.sleep(0.1)
    finally:
        pwm.stop()


def kurkure():
    servo_pin = 4
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(0)
    try:
        for _ in range(1):
            pwm.ChangeDutyCycle(12)  # 0 degrees
            time.sleep(0.1)
            pwm.ChangeDutyCycle(7.5)  # 90 degrees (neutral position)
            time.sleep(0.1)
            pwm.ChangeDutyCycle(12.5)  # 180 degrees
            time.sleep(0.1)
    finally:
        pwm.stop()


def Lays():
    servo_pin = 14
    GPIO.setup(servo_pin, GPIO.OUT)
    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(0)
    try:
        for _ in range(1):
            pwm.ChangeDutyCycle(12)  # 0 degrees
            time.sleep(0.1)
            pwm.ChangeDutyCycle(7.5)  # 90 degrees (neutral position)
            time.sleep(0.1)
            pwm.ChangeDutyCycle(12.5)  # 180 degrees
            time.sleep(0.1)
    finally:
        pwm.stop()


def receivedPayments():
    csvFile = '/home/siesgst/Desktop/Vending Payment Records_CiiA/report_2311.csv'
    searchWord1 = 'INDBNK'
    colNumber1 = 2

    searchWord2 = 'credited'
    colNumber2 = 4

    def is_transaction_within_time_range(date_time):
        current_time = datetime.now()
        time_range_start = current_time - timedelta(minutes=0.5)
        time_range_end = current_time + timedelta(minutes=1)

        formatted_time_range_start = time_range_start.strftime(
            '%Y-%m-%d %H:%M:%S.%f')[:-3]
        formatted_time_range_end = time_range_end.strftime(
            '%Y-%m-%d %H:%M:%S.%f')[:-3]

        return str(formatted_time_range_start) <= str(date_time) <= str(formatted_time_range_end)

    try:
        with open(csvFile, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)

            for row_number, row in enumerate(reader, start=1):
                if len(row) > colNumber1 and len(row) > colNumber2:
                    if searchWord1 in row[colNumber1] and searchWord2 in row[colNumber2]:
                        row_data_col2 = row[colNumber1].split()
                        row_data_col4 = row[colNumber2].split()
                        date_time = row[1]
                        try:
                            data_12 = row_data_col4[12]
                        except IndexError:
                            data_12 = "N/A"

                        global amount
                        amount = row_data_col4[0].split("Rs.")

                        if is_transaction_within_time_range(date_time) and float(amount[1]) == 5 and '@' in data_12:
                            return "Cadbury"
                        elif is_transaction_within_time_range(date_time) and float(amount[1]) == 10 and '@' in data_12:
                            return "Kitkat"
                        elif is_transaction_within_time_range(date_time) and float(amount[1]) == 20 and '@' in data_12:
                            return "True"

    except FileNotFoundError:
        print(f"The file '{csvFile}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Return None if no matching transaction is found
    return None


def generate_qr_code(myUPI, file_name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(myUPI)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_name)


time_range_start = '2021-11-16 01:24:59.132'
time_range_end = '2021-11-16 01:24:59.132'


def close_window(root, file_name):
    root.destroy()
    os.remove(file_name)


def open_and_close_qr_code(file_name):
    def check_payments_and_close(root, file_name):
        while True:
            if receivedPayments() == "Cadbury" or receivedPayments() == "Kitkat" or receivedPayments() == "True":
                root.after(0, lambda: close_window(root, file_name))
                break

    root = tk.Tk()
    root.title("QR Code Viewer")

    qr_code_image = Image.open(file_name)
    qr_code_photo = ImageTk.PhotoImage(qr_code_image)

    label = tk.Label(root, image=qr_code_photo)
    label.pack()

    # Start a thread to check for payments and close the window when received
    thread = threading.Thread(target=check_payments_and_close, args=(root, file_name))
    thread.start()

    root.mainloop()


global transaction_code, amt, product



def keypadVendingMachine():
    transaction_code = generate_transaction_code()

    if is_transaction_code_unique(transaction_code):
        product = selectProductKeypad()
        if "cadbury" in str(product).lower():
            myUPI = "upi://pay?pa=benroman1712345@okicici&pn=Amit%20Chaurasiya&am=05.00&tn=To%20Vending%20Machine%20For%20Cadbury&cu=INR"
            qr_code_file_name = "myUPIid(Cadbury).png"
            generate_qr_code(myUPI, qr_code_file_name)
            print("Recognized text:", product)
            say("Please do the Payment of Cadbury.", lang)
            say(paymentMethodOptions(), lang)
            open_and_close_qr_code(qr_code_file_name)
            say("It will take sometime to process your payment.", lang)
            while True:
                if receivedPayments() == "Cadbury":
                    say("Payment received of Rupees " + str(amount[1])[
                        :-3] + ". cadbury is being dispensed from the vending Machine. Please collect your Cadbury",
                        lang)
                    time.sleep(3)
                    save_transaction_code(transaction_code, product, amt)
                    dairyMilk()
                    say(thankYouMessages(), lang)
                    time.sleep(5)
                    return "Vended"
                    # break
                else:
                    print("No Payment Received")
                    time.sleep(15)

        elif "kitkat" in str(product).lower():
            myUPI = "upi://pay?pa=benroman1712345@okicici&pn=Amit%20Chaurasiya&am=10.00&tn=To%20Vending%20Machine%20For%20kitkat&cu=INR"
            qr_code_file_name = "myUPIid(kitkat).png"
            generate_qr_code(myUPI, qr_code_file_name)
            print("Recognized text:", product)
            say("Please do the Payment of kitkat.", lang)
            say(paymentMethodOptions(), lang)
            open_and_close_qr_code(qr_code_file_name)
            say("It will take sometime to process your payment.", lang)
            while True:
                if receivedPayments() == "Kitkat":
                    say("Payment received of Rupees " + str(amount[1])[
                        :-3] + ". Kitkat is being dispensed from the vending Machine. Please collect your Kitkat",
                        lang)
                    time.sleep(3)
                    save_transaction_code(transaction_code, product, amt)
                    Kitkat()
                    say(thankYouMessages(), lang)
                    time.sleep(5)
                    return "Vended"
                    # break
                else:
                    print("No Payment Received")
                    time.sleep(15)

        elif "kurkure" in str(product).lower():
            myUPI = "upi://pay?pa=benroman1712345@okicici&pn=Amit%20Chaurasiya&am=20.00&tn=To%20Vending%20Machine%20For%20kurkure&cu=INR"
            qr_code_file_name = "myUPIid(kurkure).png"
            generate_qr_code(myUPI, qr_code_file_name)
            print("Recognized text:", product)
            say("Please do the Payment of kurkure.", lang)
            say(paymentMethodOptions(), lang)
            open_and_close_qr_code(qr_code_file_name)
            say("It will take sometime to process your payment.", lang)
            while True:
                if receivedPayments() == "True":
                    say("Payment received of Rupees " + str(amount[1])[
                        :-3] + ". Kurkure is being dispensed from the vending Machine. Please collect your kurkure",
                        lang)
                    time.sleep(3)
                    save_transaction_code(transaction_code, product, amt)
                    kurkure()
                    say(thankYouMessages(), lang)
                    time.sleep(5)
                    return "Vended"
                    # break
                else:
                    print("No Payment Received")
                    time.sleep(15)

        elif "lays" in str(product).lower():
            myUPI = "upi://pay?pa=benroman1712345@okicici&pn=Amit%20Chaurasiya&am=20.00&tn=To%20Vending%20Machine%20For%20Lays&cu=INR"
            qr_code_file_name = "myUPIid(lays).png"
            generate_qr_code(myUPI, qr_code_file_name)
            print("Recognized text:", product)
            say("Please do the Payment of Lays.", lang)
            say(paymentMethodOptions(), lang)
            open_and_close_qr_code(qr_code_file_name)
            say("It will take sometime to process your payment.", lang)
            while True:
                if receivedPayments() == "True":
                    say("Payment received of Rupees " + str(amount[1])[
                        :-3] + "Lays is being dispensed from the vending Machine. Please collect your Lays",
                        lang)
                    time.sleep(3)
                    save_transaction_code(transaction_code, product, amt)
                    Lays()
                    say(thankYouMessages(), lang)
                    time.sleep(5)
                    return "Vended"
                    # break
                else:
                    print("No Payment Received")
                    time.sleep(15)

        elif "keep quiet" in product:
            say("shutting down..", lang)
            time.sleep(3)
            exit(0)

        else:
            say("Didn't recognise your command, please say it again.", lang)


def voiceVendingMachine():
    transaction_code = generate_transaction_code()

    if is_transaction_code_unique(transaction_code):

        command = recognize_speech()
        if "cadbury" in str(command).lower():
            myUPI = "upi://pay?pa=benroman1712345@okicici&pn=Amit%20Chaurasiya&am=05.00&tn=To%20Vending%20Machine%20For%20Cadbury&cu=INR"
            qr_code_file_name = "myUPIid(Cadbury).png"
            generate_qr_code(myUPI, qr_code_file_name)
            print("Recognized text:", command)
            say("Please do the Payment of Cadbury.", lang1)
            say(paymentMethodOptions(), lang1)
            open_and_close_qr_code(qr_code_file_name)
            say("It will take sometime to process your payment.", lang1)
            print(receivedPayments())
            while True:
                if receivedPayments() == "Cadbury":
                    product = "Cadbury"
                    amt = float(amount[1])
                    save_transaction_code(transaction_code, product, amt)
                    say("Payment received of Rupees " + str(amount[1])[
                                                        :-3] + " cadbury is being dispensed from the vending Machine. Please collect your cadbury",
                        lang1)
                    time.sleep(3)
                    dairyMilk()
                    say(thankYouMessages(), lang1)
                    time.sleep(5)
                    # break
                    return "Vended"
                else:
                    print("No Payment Received")
                    time.sleep(15)

        elif "kitkat" in str(command).lower():
            myUPI = "upi://pay?pa=benroman1712345@okicici&pn=Amit%20Chaurasiya&am=10.00&tn=To%20Vending%20Machine%20For%20kitkat&cu=INR"
            qr_code_file_name = "myUPIid(kitkat).png"
            generate_qr_code(myUPI, qr_code_file_name)
            print("Recognized text:", command)
            say("Please do the Payment of kitkat.", lang1)
            say(paymentMethodOptions(), lang1)
            open_and_close_qr_code(qr_code_file_name)
            say("It will take sometime to process your payment.", lang1)
            while True:
                if receivedPayments() == "Kitkat":
                    product = "Kitkat"
                    amt = float(amount[1])
                    save_transaction_code(transaction_code, product, amt)
                    say("Payment received of Rupees " + str(amount[1])[
                                                        :-3] + ". Kitkat is being dispensed from the vending Machine. Please collect your Kitkat",
                        lang1)
                    time.sleep(3)
                    Kitkat()
                    say(thankYouMessages(), lang1)
                    time.sleep(5)
                    # break
                    return "Vended"
                else:
                    print("No Payment Received")
                    time.sleep(15)

        elif "kurkure" in str(command).lower():
            myUPI = "upi://pay?pa=benroman1712345@okicici&pn=Amit%20Chaurasiya&am=20.00&tn=To%20Vending%20Machine%20For%20kurkure&cu=INR"
            qr_code_file_name = "myUPIid(kurkure).png"
            generate_qr_code(myUPI, qr_code_file_name)
            print("Recognized text:", command)
            say("Please do the Payment of kurkure.", lang1)
            say(paymentMethodOptions(), lang1)
            open_and_close_qr_code(qr_code_file_name)
            say("It will take sometime to process your payment.", lang1)
            while True:
                if receivedPayments() == "True":
                    product = "Kurkure"
                    amt = float(amount[1])
                    save_transaction_code(transaction_code, product, amt)
                    say("Payment received of Rupees " + str(amount[1])[
                                                        :-3] + ". Kurkure is being dispensed from the vending Machine. Please collect your kurkure",
                        lang1)
                    time.sleep(3)
                    kurkure()
                    say(thankYouMessages(), lang1)
                    time.sleep(5)
                    # break
                    return "Vended"
                else:
                    print("No Payment Received")
                    time.sleep(15)

        elif "lays" in str(command).lower():
            myUPI = "upi://pay?pa=benroman1712345@okicici&pn=Amit%20Chaurasiya&am=20.00&tn=To%20Vending%20Machine%20For%20Lays&cu=INR"
            qr_code_file_name = "myUPIid(lays).png"
            generate_qr_code(myUPI, qr_code_file_name)
            print("Recognized text:", command)
            say("Please do the Payment of Lays.", lang1)
            say(paymentMethodOptions(), lang1)
            open_and_close_qr_code(qr_code_file_name)
            say("It will take sometime to process your payment.", lang1)
            while True:
                if receivedPayments() == "True":
                    product = "Lays"
                    amt = float(amount[1])
                    save_transaction_code(transaction_code, product, amt)
                    say("Payment received of Rupees " + str(amount[1])[
                                                        :-3] + "Lays is being dispensed from the vending Machine. Please collect your Lays",
                        lang1)
                    time.sleep(3)
                    Lays()
                    say(thankYouMessages(), lang1)
                    time.sleep(5)
                    # break
                    return "Vended"
                else:
                    print("No Payment Received")
                    time.sleep(15)

        elif "keep quiet" in command:
            say("shutting down..", lang1)
            time.sleep(3)
            exit(0)

        else:
            say("Didn't recognise your command, please say it again.", lang1)


global lang, lang1, inputMethod


while True:
    try:
        inputMethod = selectInputMethod()
        if inputMethod == "Manual":
            lang = selectLanguageKeypad()
            say(welcomeMessages(), lang)
            while True:
                if keypadVendingMachine() == "Vended":
                    break
                else:
                    continue

        elif inputMethod == "voice":
            lang1 = selectLanguageVoice()
            say(welcomeMessages(), lang1)
            say(availableProducts(), lang1)
            while True:
                if voiceVendingMachine() == "Vended":
                    break
                else:
                    continue
    except TypeError:
        if inputMethod == "Manual":
            say("Did not recognise what you said.", lang)
        elif inputMethod == "voice":
            say("Did not recognise what you said.", lang1)
        time.sleep(5)
