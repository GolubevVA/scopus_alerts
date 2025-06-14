import logging
import sys

COLORS = {
    'RESET': '\033[0m',
    'BOLD': '\033[1m',
    'RED': '\033[31m',
    'GREEN': '\033[32m',
    'YELLOW': '\033[33m',
    'BLUE': '\033[34m',
    'MAGENTA': '\033[35m',
    'CYAN': '\033[36m',
    'WHITE': '\033[37m',
}

class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors and includes:
    - Timestamp
    - Log level
    - Module, function, and line number
    - Message
    """
    format_str = "%(asctime)s [%(levelname)s] [%(module)s:%(funcName)s:%(lineno)d] - %(message)s"
    
    FORMATS = {
        logging.DEBUG: COLORS['BLUE'] + format_str + COLORS['RESET'],
        logging.INFO: COLORS['GREEN'] + format_str + COLORS['RESET'],
        logging.WARNING: COLORS['YELLOW'] + format_str + COLORS['RESET'],
        logging.ERROR: COLORS['RED'] + format_str + COLORS['RESET'],
        logging.CRITICAL: COLORS['BOLD'] + COLORS['RED'] + format_str + COLORS['RESET']
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

logger = logging.getLogger()

def setup_logging(log_level_name: str = "INFO") -> logging.Logger:
	"""
	Sets up the logging configuration with colored output.
	
	Args:
		log_level (str): The logging level as a string (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
	"""
	log_level = getattr(logging, log_level_name.upper(), logging.INFO)
	logger.setLevel(log_level)

	console_handler = logging.StreamHandler(sys.stdout)
	console_handler.setFormatter(ColoredFormatter())
	logger.addHandler(console_handler)

	logger.propagate = False
    
	return logger

def get_logger() -> logging.Logger:
	"""
	Returns the logger. Sets it up if it has no handlers.
	
	Returns:
		logging.Logger: The logger instance.
	"""
	if not logger.hasHandlers():
		setup_logging()
	return logger
