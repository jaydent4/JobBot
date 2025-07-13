from logging_config import setup_logging

logger = setup_logging("args", "ERROR", "ERROR", "args.log")

ARG_TYPES = {
    "--time",
    "--company"
    "--role",
    "--location"
}

# pass arguments in a 10-tuple
# (id,company_name,role,location,application_link,date_posted,time_posted,date_scraped,time_scraped,scrape_source)
ARGS_SIZE = 10
ID = 0
COMPANY_NAME = 1
ROLE = 2
LOCATION = 3
APPLICATION_LINK = 4
DATE_POSTED = 5
TIME_POSTED = 6
DATE_SCRAPED = 7
TIME_SCRAPED = 8
SCRAPED_SOURCES = 9

"""
validates arguments
Args:
    args: tuple, arguments passed from discord bot
Returns:
    bool
"""

def validate(args) -> bool:
    if not args:
        logger.error('no args were provided')
        return False
    
    current_arg_type = None
    for arg in args:
        if not current_arg_type and not arg.startswith("--"):
            logger.error('arg found with no matching arg type')
            return False
        if current_arg_type and arg.startswith("--"):
            logger.error('arg type cannot be passed as an argument')
            return False
        if arg.startswith("--") and arg not in ARG_TYPES:
            logger.error('arg type is invalid') 
            return False       


        # sorry this code looks so ugly
        if arg.startswith("--"):
            current_arg_type = arg
        else:
            if current_arg_type == "--time":
                if not arg.isdigit():
                    logger.error('arg of arg type \'--time\' must be a valid integer')
                    return False
                if int(args) < 0:
                    logger.error('arg of arg type \'--time\' must be greater than 0')
                    return False
    return True

"""
parses args in order of database columns
Args:
    args: tuple
Returns:
    tuple
"""
def parse(args) -> tuple:
    parsed_args = [None] * ARGS_SIZE
    current_arg_type = None
    for arg in args:
        if arg.startswith("--"):
            current_arg_type = arg[2:]
        else:
            match current_arg_type:
                case "time":
                    parsed_args[TIME_POSTED] = arg
                case "company":
                    parsed_args[COMPANY_NAME] = arg
                case "role":
                    parsed_args[ROLE] = arg
                case "location":
                    parsed_args[LOCATION] = arg
            current_arg_type = None
    logger.info(f'Parsed args: {parsed_args}')
    return tuple(parsed_args)
                
                

    
