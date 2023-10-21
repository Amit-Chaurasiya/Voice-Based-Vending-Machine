import random


def thanks_for_shopping():
    thanks_messages = [
        "Thank you for choosing us for your snack break!"
        "Your satisfaction is our delight. Thanks for shopping with us!"
        "A big 'thank you' for making us your snack destination!"
        "We're grateful for your purchase. Enjoy your treats!"
        "Thanks for being a part of our vending machine family."
        "Your choice makes us smile. Thanks for shopping with us!"
        "Your snack adventure starts here. Thanks for choosing us!"
        "We're delighted you stopped by. Thanks for shopping!"
        "Your support means the world to us. Thank you for your purchase!"
        "As your snacks are dispensed, our gratitude is also delivered. Thank you!"
        "We're vending happiness, and you've made our day. Thank you!"
        "Your choice makes us vending happy. Thanks for your patronage!"
    ]

    random_message = random.choice(thanks_messages)
    return random_message


# Call the function to print a random message
thanks_for_shopping()
