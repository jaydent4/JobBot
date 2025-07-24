import logging
import os

def setup_logging(name: str, log_level: str, file_level: str, log_file='bot.log') -> logging.Logger:

    """
    Returns logging.Logger, creates logger with console and file configurations
    Args:
        name: name of the logger
        log_level: minimum level of log to output on logger and on console
        file_level: minimum level of log to output on file
        log_file: name of log (do not include full path)
    """    


    # Configure logger
    logger = logging.getLogger(name)
    match log_level:
        case "DEBUG":
            logger.setLevel(logging.DEBUG)
        case "INFO":
            logger.setLevel(logging.INFO)
        case "WARNING":
            logger.setLevel(logging.WARNING)
        case "ERROR":
            logger.setLevel(logging.ERROR)
        case "CRITICAL":
            logger.setLevel(logging.CRITICAL)
        case _:
            logger.setLevel(logging.INFO)
    
    # If handlers exist, return logger (do not re-add handlers)
    if logger.hasHandlers():
        return logger
    
    # Format log statements
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Initialize console handler
    console_handler = logging.StreamHandler()
    match log_level:
        case "DEBUG":
            console_handler.setLevel(logging.DEBUG)
        case "INFO":
            console_handler.setLevel(logging.INFO)
        case "WARNING":
            console_handler.setLevel(logging.WARNING)
        case "ERROR":
            console_handler.setLevel(logging.ERROR)
        case "CRITICAL":
            console_handler.setLevel(logging.CRITICAL)
        case _:
            console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Initialize file handler
    log_file_path = os.path.join('log/', log_file)
    file_handler = logging.FileHandler(log_file_path, mode='a', encoding='utf-8')
    match file_level:
        case "DEBUG":
            file_handler.setLevel(logging.DEBUG)
        case "INFO":
            file_handler.setLevel(logging.INFO)
        case "WARNING":
            file_handler.setLevel(logging.WARNING)
        case "ERROR":
            file_handler.setLevel(logging.ERROR)
        case "CRITICAL":
            file_handler.setLevel(logging.CRITICAL)
        case _:
            file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

