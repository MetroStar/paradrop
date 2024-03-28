#!/usr/bin/env python3
from random import choices
from string import ascii_letters, digits


def gen_id() -> str:
    """
    Function to generate random id.
    """
    return ''.join(choices(ascii_letters + digits, k=16))
