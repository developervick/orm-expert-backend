from random import randint
from django.core.mail import send_mail


def send_otp_on_mail(recipient, otp):
    try:
        send_mail(
            'OTP',
            f'Your OTP is: {otp}',
            'HvHd9@example.com',
            [recipient],
        )
    except Exception as e:
        print(e)
        return False


def generate_random_otp(digit:int = 4) -> int:
    """
    Generates a random OTP with a given number of digits.

    Args:
        digit (int): The number of digits for the OTP. Defaults to 4.

    Returns:
        int: A random OTP with the given number of digits.
    """
    if digit == 6:
        return randint(100000, 999999)
    return randint(1000, 9999)