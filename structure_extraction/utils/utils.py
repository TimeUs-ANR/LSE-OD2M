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


def report(warn_list, topic):
    """Use logging to print messages in the terminal with different formats depending on the topic.

    :param warn_list: list of warning messages
    :type warn_list: list
    :param topic: topic of the warnings
    :type topic: string
    :return:
    """
    logging.basicConfig(format='%(levelname)s:%(message)s')
    if topic == "SIGNATURE":
        for warn_id, warn_string in warn_list:
            message = "Might be a {} but was left in the output: '{}':\n\t{}".format(
                colored(topic, "yellow"),
                colored(warn_id, "yellow"),
                colored(warn_string, "white", attrs=["dark"])
            )
            logging.warning(message)

    elif topic == "HEADER":
        for warn_id, warn_string, corr in warn_list:
            message = "Might be a {} but was left in the output: '{}':\n\t{}\n\tis it the header: '{}'?".format(
                colored(topic, "yellow"),
                colored(warn_id, "yellow"),
                colored(warn_string, "white", attrs=["dark"]),
                colored(corr, "white", attrs=["dark"])
            )
            logging.warning(message)

    elif topic == "CORRECT_HEADER":
        for warn_id, head_orig, head_corr in warn_list:
            message = "You may want to verify this correction I made in '{}':\n\tfrom: {}\n\tto  : {}".format(
                colored(warn_id, "blue"),
                colored(head_orig, "white", attrs=["dark"]),
                colored(head_corr, "white", attrs=["dark"])
            )
            logging.warning(message)
