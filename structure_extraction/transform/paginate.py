# -*- coding: utf-8 -*-

# this module calculate the correct page numbers to match the book's pagination, based on the @pagenb that
# could be retrieved from the OCR

from bs4 import BeautifulSoup
import logging

from ..utils import utils


def is_coherent(orig, new):
    """Calculate how much the original and the new list match (ignoring 'empty' page numbers marked as "x") and return an assessment based on a limit of 10% of difference.

    :param orig: original list
    :type orig: list
    :param new: new list
    :type new: list
    :return: True if matching, False if not matching enough
    """
    not_matching = 0
    for i in range(len(new)):
        if new[i] != orig[i]:
            if orig[i] != "x":
                not_matching += 1
    if not_matching/len(new) > 0.1:  # placing a limit at 10% of difference
        return False
    else:
        return True


def set_limit(list_of_int_and_str):
    """Calculate the maximum number of integers in a given list

    :param list_of_int_and_str: list of page numbers and xs
    :return: number of integers in the list
    ;rtype: integer
    """
    # This is used to set a limit for the iteration on the list of page numbers
    counter = 0
    for item in list_of_int_and_str:
        if utils.is_number(item):
            counter += 1
    return counter-1


def build_new_pagination(anchor, list_of_page_numbers):
    """Build a new list of page numbers from an anchor used as a starting point

    # Uses a step of 1
    # Will go from 0 to x, before and after the anchor

    :param anchor: index of the anchor in the list
    :type anchor: int
    :param list_of_page_numbers: list to modify
    :type list_of_page_numbers: list
    :return: new list of page number
    :rtype: list
    """
    new_pagination = list_of_page_numbers[:]
    starting_point = new_pagination[anchor]
    # building page number before the anchor
    anchor_left = anchor - 1
    new_page_nb = starting_point -1
    while anchor_left >= 0:
        new_pagination[anchor_left] = new_page_nb
        if new_page_nb > 0: # pages before 1 will all be numbered as 0 (out of range)
            new_page_nb -= 1
        anchor_left -= 1
    # building page numbers after the anchor
    anchor_right = anchor + 1
    new_page_nb = starting_point +1
    while anchor_right < len(list_of_page_numbers):
        new_pagination[anchor_right] = new_page_nb
        new_page_nb += 1
        anchor_right += 1
    return new_pagination


def get_anchor(list_of_page_numbers, which_anchor):
    """Calculate an anchore to match the first (or later) integer in a list, where empty elements are marked as "x"

    :param list_of_page_numbers: list of page numbers
    :type list_of_page_numbers: list
    :param which_anchor: indication of which integer is needed
    :type which_anchor: int
    :return: False if no anchor found, index if anchor found
    :rtype: Boolean or Int
    """
    is_nb = False
    counter = 0
    counter_true = 0
    while counter != len(list_of_page_numbers) and is_nb is False:
        is_nb = utils.is_number(list_of_page_numbers[counter])
        if is_nb is False:
            counter += 1
        else:
            if counter_true == which_anchor:
                first_nb_idx = counter
                return first_nb_idx
            else:
                is_nb = False
                counter += 1
                counter_true += 1
    return False


def list_page_numbers(soup):
    """Make a list of page numbers from a parsed XML Tree made of several page elements some of which have @pagenb attributes

    :param soup: parsed XML Tree
    :type soup: bs4.BeautifulSoup
    :return: list of page numbers
    :rtype: list
    """
    pagenumber_tracker = []
    all_pages = soup.find_all("page")
    for page in all_pages:
        if "pagenb" in page.attrs:
            pagenumber_tracker.append(int(page["pagenb"]))
        else:
            pagenumber_tracker.append("x")
    return pagenumber_tracker


def paginate(soup):
    """Takes a parsed XML Tree containing pages, some of which have @pagenb attributes which may or may not be correct and calculate the correct pagination

    This pagination matches the one displayed in the book from which the XML Tree was produced, it does not simply match the indexation of the page elements in the tree.
    The value in @pagenb attributes was produced through OCR, which is the reason why it may or may not be correct.
    We do this because we want to be able to find which book page the page elements corresponds to.

    :param soup: parsed XML Tree
    :type soup: bs4.BeautifulSoup
    :return: parsed XML Tree
    :rtype: bs4.BeautifulSoup
    """
    logging.basicConfig(format='%(levelname)s:%(message)s')  # setting format for logging

    orig_pagination = list_page_numbers(soup)
    if len(orig_pagination) > 0:
        max_iterations = set_limit(orig_pagination)  # will not iterate more times than there are possible anchors in the list of page numbers
        if max_iterations >= 0:
            iterating = 0  # iterating is used to set which anchor we look for
            anchor = get_anchor(orig_pagination, 0)
            if anchor:
                error_margin = False
                while error_margin is False and iterating < max_iterations:
                    new_pagination = build_new_pagination(anchor, orig_pagination)
                    error_margin = is_coherent(orig_pagination, new_pagination)
                    iterating += 1
                    anchor = get_anchor(orig_pagination, iterating)
                # ajouter l'attribution des nouvelles valeurs de pagination à la soupe
                # renvoyer la soupe !
            else:
                # this means there is no integer in the list of page numbers
                logging.warning("Could not calculate new pagination.")
                return soup
        else:
            # this means there is no integer in the list of page numbers
            logging.warning("Could not calculate new pagination.")
            return soup
    else:
        # this means there is no integer in the list of page numbers
        logging.warning("Could not calculate new pagination.")
        return soup
