# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from termcolor import colored

def make_the_soup(filename):
    """Read an xml document and return its content as a bs4 object

    :param filename: filename
    :return: content of the document or False
    :rtype: bs4.BeautifulSoup or boolean
    """
    # Parsing the XML file with lxml-xml used to work but no longer does
    # We are therefore parsing the input file with HTML (lxml)
    # which implies the following modifications:
    # - empty elements are open/close
    # - attributes are all lowercase
    # - the tree begins with extra html/body/... elements
    try:
        with open(filename, "r") as f:
            text = f.read()
        soup = BeautifulSoup(text, "lxml")
    except Exception as e:
        print(colored("Error", "red", attrs=["bold"]), e)
    return soup