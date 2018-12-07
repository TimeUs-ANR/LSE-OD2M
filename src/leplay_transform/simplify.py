# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

def rearrange(soup):
    """Simplify XML ABBY structure and sort text blocks from other types of blocks

    :param soup: parsed XML tree
    :type soup: bs4.BeautifulSoup
    :return: parsed XML tree
    :rtype: bs4.BeautifulSoup
    """
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
                # finding a way around to delete tag named text
                # because tag.text means something to bs4
                all_tags = block.contents
                for tag in all_tags:
                    if tag.name == "text":
                        tag.decompose()
                # moving line elements right under par element
                all_lines = block.find_all("line")
                for line in all_lines:
                    all_formatting = line.find_all("formatting")
                    one_string = []
                    for formatting in all_formatting:
                        one_string.append(formatting.string)
                        formatting.decompose()
                    line.append(" ".join(one_string))
                block["type"] = "Text"
                del block["blockname"]
                block.name = "div"
    return soup