# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
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

    try:
        with open(input, "r") as f:
            text_input = f.read()
        soup = BeautifulSoup(text_input, "lxml")
    except Exception as e:
        print("Error: ", e)

    all_pages = soup.find_all("page")

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
    # preparing alternative soup with only removed items
    guard = """<html><document xmlns="http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml" version="1.0" producer="timeUs"></document></html>"""
    guard_soup = BeautifulSoup(guard, "lxml")
    all_pages = soup.find_all("page")
    count = 0
    for page in all_pages:
        count += 1
        page["id"] = "page%s" % count
        page_f = copy(page)
        page_f.clear()
        all_divs = page.find_all("div")
        div_count = 0
        for div in all_divs:
            div_count += 1
            div["id"] = "page%s_d%s" % (count, div_count)
            div_f = copy(div)
            div_f.clear()
            all_ps = div.find_all("p")
            p_count = 0
            for p in all_ps:
                p_count += 1
                p["id"] = "page%s_d%s_p%s" % (count, div_count, p_count)
                p_f = copy(p)
                p_f.clear()
                all_lines = p.find_all("line")
                for line in all_lines:
                    # targetting headers
                    if int(line["b"]) < (int(page["height"]) * 0.12):
                        if (int(line.parent["linespacing"]) <= 750) and (int(line.parent["linespacing"]) >= 390):
                            line_f = line.extract()
                            line_f["type"] = "header"
                            p_f.append(line_f)
                    # targetting signatures
                    elif int(line["b"]) > (int(page["height"]) * 0.91):
                        if len(line.string) < 2:
                            line_f = line.extract()
                            line_f["type"] = "signature"
                            p_f.append(line_f)
                if len(p_f.contents) > 0:
                    div_f.append(p_f)
            if len(div_f.contents) > 0:
                page_f.append(div_f)
        guard_soup.document.append(page_f)

    # ...
    # - recompose paragraphs
    # - identify title
    # - add management of location within the article from titles and headers

    final_str = str(soup.prettify())
    guard_str = str(guard_soup.prettify())

    # Making name for output file
    if not output:
        input = input.split(".")
        output = str(input[0]) + "_out.xml"
        output_guard = str(input[0]) + "_guard.xml"
    else:
        output = output[0].split(".")
        output = str(output[0]) + ".xml"
        output_guard = str(output[0]) + "_guard.xml"
    # writing output
    with open(output, "w") as f:
        f.write(final_str)
    with open(output_guard, "w") as f:
        f.write(guard_str)

    return


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transform XML files to raw text.")
    parser.add_argument("-i", "--input", action="store", required=True, nargs=1, help="path to file to transform.")
    parser.add_argument("-o", "--output", action="store", nargs=1,
                        help="desired path to resulting filename. Default : input filename + '_out.xml | _guard.xml.'")
    args=parser.parse_args()

    make_text(input=args.input[0], output=args.output)