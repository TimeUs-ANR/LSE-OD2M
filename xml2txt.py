# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re

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
        soup = BeautifulSoup(text_input, "lxml")
        pages = soup.find_all("page")
        text_output = []
        for page in pages:
            # adding marker
            text_output.append("\n===PAGE===\n\n")
            blocs = page.find_all("block")
            for bloc in blocs:
                # adding markers for tables
                if bloc["blocktype"] == "Table":
                    text_output.append("\n[--Tableblock--]\n\n")
                elif bloc["blocktype"] == "Text":
                    paragraphs = bloc.find_all("par")
                    for paragraph in paragraphs:
                        paragraph = paragraph.find_all("formatting")
                        # removing extra spaces and resolving hyphenation
                        p = "\n".join(["%s" % line.string for line in paragraph])
                        p = re.sub(r"^ +", "", p, flags=re.M)
                        p = re.sub(r"¬\n|-\n", "", p, flags=re.M)
                        p = re.sub(r"\n", " ", p, flags=re.M)
                        text_output.append(p)
                        text_output.append("\n\n")
        text_output_str = "".join(text_output)

        # Making name for output file
        if not output:
            input = input.split(".")
            output = str(input[0]) + ".txt"
        else:
            output = output[0].split(".")
            output = str(output[0]) + ".txt"

        # writing output
        with open(output, "w") as f:
            f.write(text_output_str)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transform XML files to raw text.")
    parser.add_argument("-i", "--input", action="store", nargs=1, help="path to file to transform.")
    parser.add_argument("-o", "--output", default="", action="store", nargs=1,
                        help="desired path to resulting filename. Default : input filename + .txt.")
    args=parser.parse_args()

    make_text(input=args.input[0], output=args.output)