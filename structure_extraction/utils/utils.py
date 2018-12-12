# -*- coding: utf-8 -*-
import logging
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
              "Might be a HEADER but was left in output : '{}':\n\t".format(warn_id),
              colored(warn_string, "white", attrs=["dark"]))
    for warn_id, warn_string in warning_signatures:
        print(colored("WARNING:", "yellow", attrs=["reverse"]),
              "Might be a SIGNATURE but was left in output : '{}':\n\t".format(warn_id),
              colored(warn_string, "white", attrs=["dark"]))

def report(warn_list, topic):
    """

    :param warn_list:
    :param topic:
    :return:
    """
    logging.basicConfig(format='%(levelname))s:%(message)s')
    if topic == "SIGNATURE":
        for warn_id, warn_string in warn_list:
            message = "Might be a {} but was left in the output: '{}':\n{}".format(
                colored(topic, "yellow"),
                colored(warn_id, "yellow"),
                colored(warn_string, "white", attrs=["dark"])
            )
            logging.warning(message)

    elif topic == "HEADER":
        for warn_id, warn_string, corr in warn_list:
            message = "Might be a {} but was left in the output: '{}':\n{}\nis it: {}".format(
                colored(topic, "yellow"),
                colored(warn_id, "yellow"),
                colored(warn_string, "white", attrs=["dark"]),
                colored(corr, "blue", attrs=["dark"])
            )
            logging.warning(message)

    elif topic == "CORRECT_HEADER":
        for warn_id, head_orig, head_corr in warn_list:
            message = "You may want to verify this correction I made in '{}':\nfrom: {}\nto  : {}".format(
                colored(warn_id, "blue"),
                head_orig,
                colored(head_corr, "white", attrs=["dark"])
            )
            logging.warning(message)
