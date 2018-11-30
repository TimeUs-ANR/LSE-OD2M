# -*- coding: utf-8 -*-

from bs4 import element as bs4_element
from bs4 import BeautifulSoup
from termcolor import colored
import re
from copy import copy


def make_text(input, output=False):
    """ Perform transformation to raw text, adding markers

    :param input: name of file to transform
    :param output: name of output file to create
    :type input: string
    :type output: list if True
    :return:
    """
    file_exists = True
    try:
        with open(input, "r") as f:
            text_input = f.read()
        soup = BeautifulSoup(text_input, "lxml-xml")
    except Exception as e:
        file_exists = False
        print(colored("Error:", "red", attrs=["bold"]), e)

    if file_exists:
        all_p = soup.find_all("page")
        all_pages = all_p[10:13]
        final_doc = BeautifulSoup("<document></document>", "lxml-xml")
        for page in all_pages:

            new_pb = BeautifulSoup("<temp><pb/></temp>", "lxml-xml")
            att_page = page.attrs
            for k in att_page:
                new_pb.pb[k] = att_page[k]
            final_doc.document.append(new_pb.pb)
            for elem_in_page in page.contents:
                if elem_in_page.name == "div":
                    print(elem_in_page.name)
                    new_div = BeautifulSoup("<temp><div></div></temp>", "lxml-xml")
                    att_div = elem_in_page.attrs
                    for k in att_div:
                        new_div.div[k] = att_div[k]

                    for elem_in_div in elem_in_page.contents:
                        if elem_in_div.name == "p":
                            new_p = BeautifulSoup("<temp><p></p></temp>", "lxml-xml")
                            att_p = elem_in_div.attrs
                            for k in att_p:
                                new_p.p[k] = att_p[k]
                            all_lines = elem_in_div.find_all("line")
                            for line in all_lines:
                                new_lb = BeautifulSoup("<temp><lb/></temp>", "lxml-xml")
                                att_line = line.attrs
                                for k in att_line:
                                    new_lb.lb[k] = line.attrs[k]
                                new_p.p.append(new_lb.lb)
                                # forced to remove BS unwanted extra spaces
                                new_p.p.append(line.string.strip("\n "))
                            new_div.div.append(new_p.p)
                        else:
                            new_div.div.append(elem_in_div)
                    final_doc.document.append(new_div.div)
                else:
                    final_doc.document.append(elem_in_page)
        #print(final_doc)

    return


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transform XML files to raw text.")
    parser.add_argument("-i", "--input", action="store", required=True, nargs=1, help="path to file to transform.")
    parser.add_argument("-o", "--output", action="store", nargs=1,
                        help="desired path to resulting filename. Default : input filename + '_out.xml | _guard.xml.'")
    args=parser.parse_args()

    make_text(input=args.input[0], output=args.output)