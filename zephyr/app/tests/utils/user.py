import random
import string


def random_string_16():
    return "".join(random.choices(string.ascii_letters, k=16))
