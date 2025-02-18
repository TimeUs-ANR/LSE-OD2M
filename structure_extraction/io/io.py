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
            soup = BeautifulSoup(f, "lxml")
    except Exception as e:
        print(colored("Error", "red", attrs=["bold"]), e)
        soup = False
    return soup


def make_out_filenames(name_input, name_output=False):
    """Create output file names

    :param name_input: filename
    :type name_input: string
    :param name_output: filename
    :type name_output: string or Boolean
    :return: filenames
    :rtype: tuple
    """
    if not name_output:
        nin = name_input.split(".")
        out_xml = str(nin[0]) + "_out.xml"
        out_guard = str(nin[0]) + "_guard.xml"
        out_txt = str(nin[0]) + ".txt"
    else:
        nout = name_output[0].split(".")
        out_xml = str(nout[0]) + ".xml"
        out_guard = str(nout[0]) + "_guard.xml"
        out_txt = str(nout[0]) + ".txt"
    return out_xml, out_guard, out_txt


def write_output(filename, content):
    """Write strings into documents

    :param filename: filename
    :type filename: string
    :param content: file content
    :type content: string
    """
    with open(filename, "w") as f:
        f.write(content)


def make_string(soup):
    """ Transform a parsed XML tree into a string

    :param soup: parsed XML tree
    :type soup: bs4.BeautifulSoup
    :rtype: string
    """
    s = str(soup.prettify())
    return s