import random
import re


def create_token():
    digits = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-"
    token = ""
    for x in range(16):
        token += random.choice(digits)
    return token


def cleanup_word(word):
    return re.sub(r"[^a-z\-']", "", word.lower())
