# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re

B_COORD = 450 # value of line's @b
LINE_LEN = 65 # maximum length of the line

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
        headers = [["chaîne", "longueur chaîne", "val line/@b"]]
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
                        paragraph = paragraph.find_all("line")
                        # isolating headers
                        clean_paragraph = []
                        for line in paragraph:
                            if int(line["b"]) <= B_COORD and len(line.formatting.string) <= LINE_LEN:
                                headers.append([line.formatting.string, len(line.formatting.string), line["b"]])
                            else:
                                clean_paragraph.append(line.formatting.string)
                        # removing extra spaces and resolving hyphenation
                        p = "\n".join(["%s" % line for line in clean_paragraph])
                        p = re.sub(r"^ +", "", p, flags=re.M)
                        p = re.sub(r"¬\n|-\n", "", p, flags=re.M)
                        p = re.sub(r"\n", " ", p, flags=re.M)
                        text_output.append(p)
                        text_output.append("\n\n")
        text_output_str = "".join(text_output)
        header_out = []
        for h in headers:
            header_out.append(";".join(["\"%s\"" % e for e in h]))
        header_out = "\n".join(header_out)
        # Making name for output file
        if not output:
            input = input.split(".")
            output = str(input[0]) + ".txt"
            header_output = str(input[0]) + "_headers.csv"
        else:
            output = output[0].split(".")
            output = str(output[0]) + ".txt"
            header_output = str(output[0]) + "_headers.csv"
        # writing output
        with open(output, "w") as f:
            f.write(text_output_str)
        with open(header_output, "w") as f:
            f.write(header_out)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transform XML files to raw text.")
    parser.add_argument("-i", "--input", action="store", required=True, nargs=1, help="path to file to transform.")
    parser.add_argument("-o", "--output", default="", action="store", nargs=1,
                        help="desired path to resulting filename. Default : input filename + .txt.")
    args=parser.parse_args()

    make_text(input=args.input[0], output=args.output)