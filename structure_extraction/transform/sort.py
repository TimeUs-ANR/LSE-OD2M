# -*- coding: utf-8 -*-

# What is a "signature"? : it is the name given to the individual markers (numbers or letters) placed in the bottom
# margins of the first page (or couple of pages) of a leaf (later folded in several pages) in an ancient book. It is used
# as a guideline to replace every leafs in the right order when binding the book.

# upgrades needed :
# - might be necessary to decompose the different transformations
# - add control of whether it's a header or not by checking if it's only a string made of numbers in the top 12%.

# what this module does:
# - create identifiers for pages, divs, ps and lines
# - sort headers from the rest of the body
# - sort signatures from the rest of the body
# - calculate the correct content of the header and give the corrected and original version as attributes to the page

from bs4 import BeautifulSoup
import stringdist

from copy import copy

from ..utils import utils
from ..ref_data import groundtruth


def correct_headers(s):
    distance = 100
    mark = ""
    for k in groundtruth.headers:
        this_distance = stringdist.levenshtein(s.replace(" ", "").lower(), groundtruth.headers[k].replace(" ", "").lower())
        if this_distance < distance:
            distance = this_distance
            mark = k
    return distance, groundtruth.headers[mark]


def exclude_headers_signatures(soup):
    """Sort headers and signatures from the body of text and give each element an id
    
    :param soup: parsed XML tree
    :rtype soup: bs4.BeautifulSoup
    :return: parsed XML trees and lists of warnings
    :rtype: tuple
    """
    guard = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><document xmlns="http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml" version="1.0" producer="timeUs"></document>"""
    guard_soup = BeautifulSoup(guard, "xml")

    all_pages = soup.find_all("page")
    warning_headers = []
    warning_signatures = []
    warning_headers_corrected = []
    count_page = 0
    # reading each individual page and its content to create identifiers (page/div/p/line)
    for page in all_pages:
        count_page += 1
        page["id"] = "page%s" % count_page
        page_f = copy(page)
        page_f.clear()
        all_divs = page.find_all("div")
        count_div = 0
        # since elements from the header can be split over several <line>s, <p>s or even <div>s
        # we make a single string to gather everything that may be part of the header
        # and clean it later in the program.
        header_string = ""
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
                    # testing the line : is it a header and needs to be taken out of the tree?
                    if int(line["b"]) < (int(page["height"]) * 0.12):
                        if "linespacing" in line.parent.attrs:
                            # for headers, lineSpacing value is normally comprehended between 390 and 750.
                            if (int(line.parent["linespacing"]) <= 750) and (int(line.parent["linespacing"]) >= 390):
                                line_f = line.extract()
                                line_f["type"] = "header"
                                p_f.append(line_f)
                                # giving page @pagenb when the pagenumber is fully OCR-ed
                                if line_f.string:
                                    if utils.is_number(line_f.string):
                                        page["pagenb"] = line_f.string
                                    else:
                                        header_string = header_string + line_f.string + " "
                        # raising warning if in the top 12% of the page and short enough
                        # (55 is, generally, the max length of the header)
                        # that is because the value of @lineSpacing is sometimes out of the normal range
                        # or because sometimes @lineSpacing does not exist
                            else:
                                count_line += 1
                                line["id"] = id_line + str(count_line)
                                dist, alt_string = correct_headers(line.string)
                                if dist < 10:
                                    warning_headers.append((line["id"], line.string, alt_string))
                        else:
                            count_line += 1
                            line["id"] = id_line + str(count_line)
                            dist, alt_string = correct_headers(line.string)
                            if dist < 10:
                                warning_headers.append((line["id"], line.string, alt_string))
                    # testing the line : is it a signature and needs to be taken out of the tree?
                    elif int(line["b"]) > (int(page["height"]) * 0.91):
                        if len(line.string.strip()) <= 2:
                            # considered a signature if in the last 9% of page height and extra short
                            line_f = line.extract()
                            line_f["type"] = "signature"
                            p_f.append(line_f)
                        elif len(line.string.strip()) >= 3 and len(line.string) < 5:
                            # raising warning if in the last 9% of page height but not short enough
                            # in case interfering characters were recognized
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
        if len(header_string) > 0:
            page["pageheader_orig"] = header_string
            dist, alt_string = correct_headers(header_string)  # where alt_string is the "correct" alternative to the string
            if dist < 10:  # if the distance is less than 10% then it is considered the right correction
                page["pageheader_corr"] = alt_string
            else:  # otherwise we still keep the suggested alternative version in the output but add a warning
                page["pageheader"] = header_string
                warning_headers_corrected.append((page["id"], header_string, alt_string))
        guard_soup.document.append(page_f)
    return guard_soup, soup, warning_headers, warning_signatures, warning_headers_corrected