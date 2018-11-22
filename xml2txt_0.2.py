# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import copy


def make_text(input, output):
    """ Perform transformation to raw text, adding markers

    :param input: name of file to transform
    :param output: name of output file to create
    :type input: string
    :type output: list if True
    :return:
    """

    try:
        with open(input, "r") as f:
            text_input = f.read()
    soup_input = BeautifulSoup(text_input, "lxml")
    soup_output = copy.deepcopy(soup_input)

    # ...

    # Making name for output file
    if not output:
        input = input.split(".")
        output = str(input[0]) + ".txt"
        output_guard = str(input[0]) + "_guard.xml"
    else:
        output = output[0].split(".")
        output = str(output[0]) + ".txt"
        output_guard = str(output[0]) + "_guard.xml"
    # writing output
    #with open(output, "w") as f:
    #    f.write(text_output_str)
    #with open(header_output, "w") as f:
    #    f.write(header_out)

    return


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transform XML files to raw text.")
    parser.add_argument("-i", "--input", action="store", required=True, nargs=1, help="path to file to transform.")
    parser.add_argument("-o", "--output", default="", action="store", nargs=1,
                        help="desired path to resulting filename. Default : input filename + '.txt' or + '_guard.xml.'")
    args=parser.parse_args()

    make_text(input=args.input[0], output=args.output)