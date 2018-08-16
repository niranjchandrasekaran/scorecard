#!/usr/bin/env python

import argparse
from readwrite.inout import Input, PrintScorecard
from readwrite.readcric import ReadCric, ProcessCric
from readwrite.convert import Convert
from scorecard.scorecard import InningsScorecard

parser = argparse.ArgumentParser(description='Generate scorecards')
parser.add_argument('-f', metavar='', help='Single yaml file or a list of yaml files')

args = parser.parse_args()


if __name__ == '__main__':
    file_input = Input()
    file_convert = Convert()

    flist = file_input.file_list(args)

    for yamlfile in flist:
        print('Generating scorecard for %s...' % str(yamlfile))
        file_convert.yaml_to_cric(yamlfile)
        cricfile = str(yamlfile)[:-4]+'cric'
        cric = ReadCric(cricfile)
        process = ProcessCric()

        info = process.process_info(cric.info)
        event = process.process_event(cric.header, cric.event)

        first_innings = InningsScorecard(event.loc[event.innings == '1'])
        second_innings = InningsScorecard(event.loc[event.innings == '2'])

        PrintScorecard(first_innings, second_innings, cricfile)

