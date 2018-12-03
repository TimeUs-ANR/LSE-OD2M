# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from termcolor import colored
import re
from copy import copy


def make_the_soup(filename):
    """Read an xml document and return its content as a bs4 object

    :param filename: filename
    :return: content of the document or False
    :rtype: bs4.BeautifulSoup or boolean
    """
    try:
        with open(filename, "r") as f:
            text = f.read()
        soup = BeautifulSoup(text, "lxml")
    except Exception as e:
        print(colored("Error", "red", attrs=["bold"]), e)
    return soup


def report_warnings(warning_headers, warning_signatures):
    """Print warnings in terminal

    :param warning_headers: list of potentially missed headers
    :param warning_signatures: list of potentially missed signatures
    """
    for warn_id, warn_string in warning_headers:
        print(colored("WARNING:", "yellow", attrs=["reverse"]),
              "Might be a HEADER but was left in output : '%s':\n\t" % (warn_id),
              colored(warn_string, "white", attrs=["dark"]))
    for warn_id, warn_string in warning_signatures:
        print(colored("WARNING:", "yellow", attrs=["reverse"]),
              "Might be a SIGNATURE but was left in output : '%s':\n\t" % (warn_id),
              colored(warn_string, "white", attrs=["dark"]))


def make_out_filenames(name_input, name_output=False):
    """Makes output filenames

    :param name_input: filename
    :type name_input: string
    :param name_output: filename
    :type name_output: string or Boolean
    :return: filenames
    :rtype: tuple
    """
    if not name_output:
        nin = name_input.split(".")
        nout = str(nin[0]) + "_out.xml"
        out_guard = str(nin[0]) + "_guard.xml"
    else:
        nout = name_output[0].split(".")
        nout = str(nout[0]) + ".xml"
        out_guard = str(nout[0]) + "_guard.xml"
    return nout, out_guard


def write_output(filename, content):
    """ Write
    :param filename: filename
    :type filename: string
    :param content: file content
    :type content: string
    """
    with open(filename, "w") as f:
        f.write(content)


def make_text(input, output=False):
    """ Perform transformation to raw text, adding markers

    :param input: name of file to transform
    :param output: name of output file to create
    :type input: string
    :type output: list if True
    :return:
    """
    soup = make_the_soup(input)
    if soup:
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
        guard = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><document xmlns="http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml" version="1.0" producer="timeUs"></document>"""
        guard_soup = BeautifulSoup(guard, "lxml-xml")
        all_pages = soup.find_all("page")
        warning_headers = []
        warning_signatures = []
        count_page = 0
        for page in all_pages:
            count_page += 1
            page["id"] = "page%s" % count_page
            page_f = copy(page)
            page_f.clear()
            all_divs = page.find_all("div")
            count_div = 0
            for div in all_divs:
                count_div += 1
                div["id"] = "page%s_div%s" % (count_page, count_div)
                div_f = copy(div)
                div_f.clear()
                all_ps = div.find_all("p")
                count_p = 0
                for p in all_ps:
                    count_p += 1
                    p["id"] = "page%s_div%s_p%s" % (count_page, count_div, count_p)
                    p_f = copy(p)
                    p_f.clear()
                    all_lines = p.find_all("line")
                    count_line = 0
                    for line in all_lines:
                        id_line = "page%s_d%s_p%s_l" % (count_page, count_div, count_p)
                        # targetting headers
                        if int(line["b"]) < (int(page["height"]) * 0.12):
                            if "linespacing" in line.parent.attrs:
                                if (int(line.parent["linespacing"]) <= 750) and (int(line.parent["linespacing"]) >= 390):
                                    line_f = line.extract()
                                    line_f["type"] = "header"
                                    p_f.append(line_f)
                                else:
                                    count_line += 1
                                    line["id"] = id_line + str(count_line)
                                    test_str = line.string
                                    if len(test_str.replace(" ", "")) < 55:
                                        warning_headers.append((line["id"], line.string))
                            else:
                                count_line += 1
                                line["id"] = id_line + str(count_line)
                                test_str = line.string
                                if len(test_str.replace(" ", "")) < 55:
                                    warning_headers.append((line["id"], line.string))
                        # targetting signatures
                        elif int(line["b"]) > (int(page["height"]) * 0.91):
                            if len(line.string) <= 2:
                                line_f = line.extract()
                                line_f["type"] = "signature"
                                p_f.append(line_f)
                            elif len(line.string) >= 3 and len(line.string) < 10:
                                count_line += 1
                                line["id"] = id_line + str(count_line)
                                warning_signatures.append((line["id"], line.string))
                            else:
                                count_line += 1
                                line["id"] = id_line + str(count_line)
                        else:
                            count_line += 1
                            line["id"] = id_line + str(count_line)
                    if len(p_f.contents) > 0:
                        div_f.append(p_f)
                if len(div_f.contents) > 0:
                    page_f.append(div_f)
            guard_soup.document.append(page_f)

        # ...
        # - recompose paragraphs
        # - identify title
        # - add management of location within the article from titles and headers

        report_warnings(warning_headers, warning_signatures)
        final_out = BeautifulSoup("", "lxml-xml")
        final_out.append(soup.document)
        final_str = str(final_out.prettify())
        guard_str = str(guard_soup.prettify())

        out_file, output_guard = make_out_filenames(input, output)
        write_output(out_file, final_str)
        write_output(output_guard, guard_str)
    return


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transform XML files to raw text.")
    parser.add_argument("-i", "--input", action="store", required=True, nargs=1, help="path to file to transform.")
    parser.add_argument("-o", "--output", action="store", nargs=1,
                        help="desired path to resulting filename. Default : input filename + '_out.xml | _guard.xml.'")
    args=parser.parse_args()

    make_text(input=args.input[0], output=args.output)