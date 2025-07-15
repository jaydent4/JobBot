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
    
    # sliding window to group args with arg types
    left = 0
    if not args[left].startswith("--"):
        logger.error('no arg type provided')
    
    curr_args: list[str] = []
    curr_arg_type = args[left]
    for right in range(1, len(args)):
        if args[right].startswith("--"):
            if len(curr_args) == 0:
                logger.error(f'no args are provided with the arg type {curr_arg_type}')
                return False
            if (curr_arg_type == "--time" or curr_arg_type == "--source") and len(curr_args) > 1:
                logger.error(f'too many args passed with arg type \'{curr_arg_type}\'')
                return False
            if args[right][2:] not in ARG_TYPES:
                logger.error('one of the args is not an option')
                return False
            curr_arg_type = args[right]
            left = right
            curr_args = []
        else:
            curr_args.append(args[right])
    return True


def parser_helper(curr_arg_type, curr_args, parsed_args):
    arg = " ".join(curr_args)
    match curr_arg_type:
        case "--time":
            parsed_args[Valid_Args.TIME.value] = ("date_posted", count_days(arg))
        case "--company":
            parsed_args[Valid_Args.COMPANY.value] = ("company_name", arg)
        case "--role":
            parsed_args[Valid_Args.ROLE.value] = ("role", arg)
        case "--location":
            parsed_args[Valid_Args.LOCATION.value] = ("location", arg)
        case "--level":
            parsed_args[Valid_Args.LEVEL.value] = ("level", arg)
        case "--count":
            parsed_args[Valid_Args.COUNT.value] = ("count", arg)
        case "--source":
            parsed_args[Valid_Args.SOURCE.value] = ("scrape_source", arg)
    return parsed_args

"""
parses args in order of valid args enum in const.py
Args:
    args: tuple
Returns:
    tuple
"""
def parse(args):
    parsed_args = [None] * Valid_Args.SIZE.value
    curr_arg_type = None
    curr_args = []
    
    # sliding window to parse
    left = 0
    if not args[left].startswith("--"):
        logger.error('no arg type provided')
    
    curr_arg_type = args[left]
    for right in range(1, len(args)):
        if args[right].startswith("--"):
            parsed_args = parser_helper(curr_arg_type, curr_args, parsed_args)
            left = right
            curr_arg_type = args[right]
            curr_args = []
        else:
            curr_args.append(args[right])
    
    parsed_args = parser_helper(curr_arg_type, curr_args, parsed_args)

    logger.info(f'Parsed args: {parsed_args}')
    return tuple(parsed_args)


def count_days(time) -> str:
    today = date.today()
    days_to_subtract = -int(time)
    past_date = today + timedelta(days=days_to_subtract)
    return past_date.strftime('%Y-%m-%d')
                
                
