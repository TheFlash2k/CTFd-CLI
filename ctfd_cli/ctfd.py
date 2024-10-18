from .utils.logger import logger
from .utils.handler import RequestHandler, Mode
from .utils.utils import get_env

class CTFd:
    def __init__(self, instance: str = "", token: str = ""):
        
        self.ctfd_instance = get_env(key="CTFD_INSTANCE", curr=instance, err_msg="CTFD_INSTANCE URL is not set")
        self.ctfd_token    = get_env(key="CTFD_ADMIN_TOKEN", curr=token, err_msg="CTFD_ADMIN_TOKEN is not set")

        if self.ctfd_instance[-1] == "/":
            self.ctfd_instance = self.ctfd_instance[:-1]
        
        if self.ctfd_instance[:7] != "http://" and self.ctfd_instance[:8] != "https://":
            self.ctfd_instance = "http://" + self.ctfd_instance

        logger.info(f"CTFd instance: {self.ctfd_instance}")
        logger.info(f"Checking connection to CTFd version.")
        if not self.is_working():
            logger.error("CTFd instance is not working.")
            exit(1)
        else:
            logger.info("CTFd instance is working.")

    def is_working(self):
        r = RequestHandler.MakeRequest(
            mode=Mode.GET,
            url=f"{self.ctfd_instance}/api/v1/users",
            token=self.ctfd_token
        )
        return r.status_code == 200