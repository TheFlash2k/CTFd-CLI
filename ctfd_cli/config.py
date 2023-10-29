import os
from dotenv import load_dotenv

def get_env(key: str, curr: str = None, default: str = None, err_msg: str = None) -> str:
    load_dotenv()
    if curr != None:
        return curr
    value = os.getenv(key, default)
    if value is None:
        raise Exception(err_msg)
    return value

## Global Config Vars
ctfd_instance = ""
ctfd_token    = ""