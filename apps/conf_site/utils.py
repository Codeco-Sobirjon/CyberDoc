import re


def check_email_or_phone(value):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, value):
        return 'email'

    phone_regex = r'^\+?\d{1,3}?\(?\d{1,4}?\)?[\d\- ]{7,15}$'
    if re.match(phone_regex, value):
        return 'phone'

    return 'invalid'
