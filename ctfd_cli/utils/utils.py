import os
from dotenv import load_dotenv
import random
import string

def random_string(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_env(key: str, curr: str = None, default: str = None, err_msg: str = None) -> str:
    load_dotenv()
    if curr != None:
        return curr
    value = os.getenv(key, default)
    if value is None:
        raise Exception(err_msg)
    return value