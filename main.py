# -*- coding: utf-8 -*-

from structure_extraction.io import io
from structure_extraction.transform import simplify, sort, breakdown, paginate
from structure_extraction.utils import utils

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transform XML files to raw text.")
    parser.add_argument("-i", "--input", action="store", required=True, nargs=1, help="path to file to transform.")
    parser.add_argument("-o", "--output", action="store", nargs=1,
                        help="desired path to resulting filename. Default : input filename + '_out.xml | _guard.xml.'")
    args = parser.parse_args()

    filename_in = args.input[0]
    filename_out = args.output

    # first we read the XML ABBY file:
    transformed_text = io.make_the_soup(filename_in)
    # !! add schema test before continuing - ABBY schema
    if transformed_text:
        # then we simplify the XML tree be sorting text and non-text blocks:
        transformed_text = simplify.rearrange(transformed_text)
        # !! add schema test before continuing -- homemade schema
        # then we sort out headers and signatures, which may raise warnings:
        transformed_text_guard, transformed_text, warning_headers, warning_signatures, warning_headers_corrected = sort.exclude_headers_signatures(transformed_text)
        paginate.paginate(transformed_text)
        # !! add schema test before continuing -- homemade schema
        # then we separate the tree structure from the physical structure of the text:
        transformed_text = breakdown.make_breakers(transformed_text)
        # !! add schema test before continuing -- homemade schema

        # raising warnings:
        utils.report(warning_headers, "HEADER")
        utils.report(warning_signatures, "SIGNATURE")
        utils.report(warning_headers_corrected, "CORRECT_HEADER")

        # creating output files content:
        final_xml_str = io.make_string(transformed_text)
        final_guard_str = io.make_string(transformed_text_guard)

        # creating output files names and writing the output:
        out_xml_file, out_guard, out_txt_file = io.make_out_filenames(filename_in, filename_out)
        io.write_output(out_xml_file, final_xml_str)
        io.write_output(out_guard, final_guard_str)

        # make plain text output
        # - recompose paragraphs
        # - identify title
        # - add management of location within the article from titles and headers
