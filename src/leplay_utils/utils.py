# -*- coding: utf-8 -*-
from termcolor import colored

def is_number(s):
    """Test if a string contains a number

    :param s: string
    :return: boolean
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def report_warnings(warning_headers, warning_signatures):
    """Print warnings in terminal

    :param warning_headers: list of potentially missed headers
    :param warning_signatures: list of potentially missed signatures
    """
    for warn_id, warn_string in warning_headers:
        print(colored("WARNING:", "yellow", attrs=["reverse"]),
              "Might be a HEADER but was left in output : '%s':\n\t" % (warn_id),
              colored(warn_string, "white", attrs=["dark"]))
    for warn_id, warn_string in warning_signatures:
        print(colored("WARNING:", "yellow", attrs=["reverse"]),
              "Might be a SIGNATURE but was left in output : '%s':\n\t" % (warn_id),
              colored(warn_string, "white", attrs=["dark"]))