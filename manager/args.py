from logging_config import setup_logging
from const import ARG_TYPES, Valid_Args
from const import ARG_TYPES
from datetime import date, timedelta

logger = setup_logging("args", "ERROR", "ERROR", "args.log")

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
    if len(args) % 2 != 0:
        logger.error('some args or arg types are not matched')
        return False

    for i in range(0, len(args) - 1, 2):
        arg_type = args[i]
        arg = args[i + 1]

        if not arg_type.startswith("--"):
            logger.error('arg type must start with \'--\'')
            return False
        if arg_type not in ARG_TYPES:
            logger.error(f'arg type {arg_type} does not exist')
            return False
        
        if arg_type == "--time":
            if not arg.isdigit():
                logger.error('arg of arg_type \'--time\' must be a valid integer')
                return False
            if int(arg) < 0:
                logger.error('arg of arg_type \'--time\' must be greater than or equal to 0')
                return False
    logger.error("valid")
    return True

"""
parses args in order of database columns
Args:
    args: tuple
Returns:
    tuple
"""
def parse(args: tuple):
    parsed_args = [None] * Valid_Args.SIZE.value
    current_arg_type = None
    for arg in args:
        if arg.startswith("--"):
            logger.error("hii")
            current_arg_type = arg[2:]
        else:
            logger.error("bye")
            match current_arg_type:
                case "time":
                    parsed_args[Valid_Args.TIME.value] = ("time_posted", count_days(arg))
                case "company":
                    parsed_args[Valid_Args.COMPANY.value] = ("company_name", arg)
                case "role":
                    parsed_args[Valid_Args.ROLE.value] = ("role", arg)
                case "location":
                    parsed_args[Valid_Args.LOCATION.value] = ("location", arg)
                case "level":
                    parsed_args[Valid_Args.LEVEL.value] = ("level", arg)
                case "count":
                    parsed_args[Valid_Args.COUNT.value] = ("count", arg)
            current_arg_type = None
    logger.error(f"hiii this is parse {parsed_args}")
    logger.info(f'Parsed args: {parsed_args}')
    return tuple(parsed_args)


def count_days(time) -> str:
    today = date.today()
    days_to_subtract = -time
    past_date = today + timedelta(days=days_to_subtract)
    return past_date.strftime('%Y-%m-%d')
                
                
