import logging
import sys

class Logger(object):

    """Logger class for logging.
    Attributes:
        name: Name of the logger
        level: Level of the logger
    Methods:
        get_logger: Returns a logger object
    
    Classes:
        Formatter: Logging Formatter to add colors and count warning / errors
    
    """

    class Formatter(logging.Formatter):
            
            """Logging Formatter to add colors and count warning / errors"""
            grey = "\x1b[38;20m"
            yellow = "\x1b[33;20m"
            blue = "\x1b[34;20m"
            red = "\x1b[31;20m"
            green = "\x1b[32;20m"
            bold_red = "\x1b[31;1m"
            reset = "\x1b[0m"
            format = "%(asctime)s %(levelname)s %(message)s"

            ### UNCOMMENT THIS FOR VERBOSITY ###
            # FORMATS = {
            #     logging.DEBUG: f"{yellow}{format.split()[0].split()[0]}{reset} {green}{format.split()[1]}{reset} {format.split()[2]}",
            #     logging.INFO: f"{yellow}{format.split()[0].split()[0]}{reset} {blue}{format.split()[1]}{reset} {format.split()[2]}",
            #     logging.WARNING: f"{yellow}{format.split()[0].split()[0]}{reset} {yellow}{format.split()[1]}{reset} {format.split()[2]}",
            #     logging.ERROR: f"{yellow}{format.split()[0].split()[0]}{reset} {red}{format.split()[1]}{reset} {format.split()[2]}",
            #     logging.CRITICAL: f"{yellow}{format.split()[0]}{reset} {bold_red}{format.split()[1]}{reset} {format.split()[2]}",
            # }

            FORMATS = {
                logging.DEBUG: f"[{green}{format.split()[1]}{reset}] {format.split()[2]}",
                logging.INFO: f"[{blue}{format.split()[1]}{reset}] {format.split()[2]}",
                logging.WARNING: f"[{yellow}{format.split()[1]}{reset}] {format.split()[2]}",
                logging.ERROR: f"[{red}{format.split()[1]}{reset}] {format.split()[2]}",
                logging.CRITICAL: f"[{bold_red}{format.split()[1]}{reset}] {format.split()[2]}",
            }
    
            def format(self, record : logging.LogRecord) -> str:

                """Format the log record.
                Args:
                    record: Log record to be formatted
                
                Returns:
                    Formatted log record
                """
                log_fmt = self.FORMATS.get(record.levelno)
                formatter = logging.Formatter(log_fmt)
                return formatter.format(record)
    
    @staticmethod
    def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
        """Returns a logger object.
        Args:
            name: Name of the logger
            level: Level of the logger
        Returns:
            A logger object.
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = Logger.Formatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

logger = Logger.get_logger(__name__, level=logging.DEBUG)