import re

def clean_email(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z ]', '', text)

    return text