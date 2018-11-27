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
        soup_in = BeautifulSoup(text_input, "lxml")
    except Exception as e:
        print("Error: ", e)

    all_pages = soup_in.find_all("page")

    for page in all_pages:
        all_blocks = page.find_all("block")
        for block in all_blocks:
            # modify figure type blocks, including tables
            if block["blocktype"] != "Text":
                block.name = "figure"
                block["type"] = block["blocktype"]
                attrs_list = block.attrs
                for attr in list(attrs_list):
                    if attr != "type":
                        del block[attr]
                block.clear()
            # rearrange text type blocks
            else:
                if block.region:
                    block.region.decompose()
                # moving par elements right under block element
                all_pars = block.find_all("par")
                for par in all_pars:
                    ext_par = par.extract()
                    ext_par.name = "p"
                    block.append(ext_par)
                # finding a way around to delete tag names text
                all_tags = block.contents
                for tag in all_tags:
                    if tag.name == "text":
                        tag.decompose()
                # moving line elements right under par element
                all_lines = block.find_all("line")
                for line in all_lines:
                    line.append(line.formatting.string)
                    f_attrs_list = line.formatting.attrs
                    if len(f_attrs_list) > 0:
                       for f_attr in f_attrs_list:
                           line[f_attr] = f_attrs_list[f_attr]
                    line.formatting.decompose()
                block["type"] = "Text"
                del block["blockname"]
                block.name = "div"


    # identifier les headers (étalonné sur s1t1enq1.xml)
    #for page in all_pages:
    #    all_lines = page.find_all("line")
    #    for line in all_lines:
    #        if int(line["b"]) < (int(page["height"]) * 0.12):
    #            if int(line.parent["linespacing"]) <= 660:
    #                print(line.parent["linespacing"], "\t", line)
    #            elif int(line.parent["linespacing"]) > 660:
    #                print(line.parent["linespacing"], "\t", line)


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