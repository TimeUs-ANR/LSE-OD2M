# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

def make_breakers(soup):
    """Transform <page></page> into <pb/> and <line></line> in <lb/>

    :param soup: parsed XML tree
    :type soup: bs4.BeautifulSoup
    :return: parsed XML tree
    :rtype: bs4.BeautifulSoup
    """
    broken_soup = BeautifulSoup("<document></document>", "xml")
    all_pages = soup.find_all("page")

    for page in all_pages:
        new_pb = BeautifulSoup("<temp><pb/></temp>", "xml")
        att_page = page.attrs
        for k in att_page:
            new_pb.pb[k] = att_page[k]
        broken_soup.document.append(new_pb.pb)

        for cont_page in page.contents:
            if cont_page.name:
                if cont_page.name == "div":
                    new_div = BeautifulSoup("<temp><div></div></temp>", "xml")
                    att_div = cont_page.attrs
                    for k in att_div:
                        new_div.div[k] = att_div[k]
                    for cont_div in cont_page.contents:
                        if cont_div.name:
                            new_p = BeautifulSoup("<temp><p></p></temp>", "xml")
                            att_p = cont_div.attrs
                            for k in att_p:
                                new_p.p[k] = att_p[k]
                            all_lines = cont_div.find_all("line")
                            for line in all_lines:
                                new_lb = BeautifulSoup("<temp><lb/></temp>", "xml")
                                att_line = line.attrs
                                for k in att_line:
                                    new_lb.lb[k] = att_line[k]
                                new_p.p.append(new_lb.lb)
                                new_p.p.append(line.string)
                            new_div.div.append(new_p.p)
                    broken_soup.document.append(new_div.div)
                else:
                    broken_soup.document.append(cont_page)
    return broken_soup