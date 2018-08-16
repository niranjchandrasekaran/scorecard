import yaml
import numpy as np


class Convert(object):

    def __init__(self):
        pass

    def yaml_to_cric(self, yamlfile):
        print('Converting ' + str(yamlfile) + '...')
        dict_file = yaml.load(open(yamlfile, 'r'))
        outfile = open(str(yamlfile)[0:-5] + '.cric', 'w')
        outfile.write('Fileid:%s\n' % str(yamlfile)[:-5])
        outfile.write('Competition:%s\n' % str(dict_file['info']['competition']))
        outfile.write('Year:%s\n' % str(dict_file['info']['dates'][0]).split('-')[0])
        outfile.write('Month:%s\n' % str(dict_file['info']['dates'][0]).split('-')[1])
        outfile.write('Day:%s\n' % str(dict_file['info']['dates'][0]).split('-')[2])
        outfile.write('MatchType:%s\n' % str(dict_file['info']['match_type']))
        outfile.write('Ground:%s\n' % str(dict_file['info']['venue']))
        outfile.write('City:%s\n' % str(dict_file['info']['city']))
        outfile.write('Team1:%s\n' % str(dict_file['info']['teams'][0]))
        outfile.write('Team2:%s\n' % str(dict_file['info']['teams'][1]))
        try:
            outfile.write('Umpire1:%s\n' % str(dict_file['info']['umpires'][0]))
            outfile.write('Umpire2:%s\n' % str(dict_file['info']['umpires'][1]))
        except KeyError:
            outfile.write('Umpire1:NA\n')
            outfile.write('Umpire2:NA\n')
        outfile.write('Toss:%s\n' % str(dict_file['info']['toss']['winner']))
        outfile.write('TossDecision:%s\n' % str(dict_file['info']['toss']['decision']))
        try:
            outfile.write('Winner:%s\n' % str(dict_file['info']['outcome']['winner']))
            try:
                outfile.write('Margin:%s runs\n' % str(dict_file['info']['outcome']['by']['runs']))
            except KeyError:
                outfile.write('Margin:%s wkts\n' % str(dict_file['info']['outcome']['by']['wickets']))
        except KeyError:
            try:
                outfile.write('Winner:%s\n' % str(dict_file['info']['outcome']['eliminator']))
            except KeyError:
                outfile.write('Winner:NA\n')
            outfile.write('Margin:%s\n' % str(dict_file['info']['outcome']['result']))
        try:
            outfile.write('MoM:%s\n' % str(dict_file['info']['player_of_match'][0]))
        except KeyError:
            outfile.write('MoM:NA\n')

        outfile.write(
            '#innings:team\tball:runs:extras:extraskind:total\tbowler:batsman:nonstriker:wicket:kind:playerout:fielder\n')
        innings_option = ['1st innings', '2nd innings']
        min_innings = np.min([2, len(dict_file['innings'])])
        for innings in range(0, min_innings):
            innings_team = dict_file['innings'][innings][innings_option[innings]]['team']
            for ballEvent in dict_file['innings'][innings][innings_option[innings]]['deliveries']:
                for balls in ballEvent:
                    batsman = ballEvent[balls]['batsman']
                    bowler = ballEvent[balls]['bowler']
                    nonstriker = ballEvent[balls]['non_striker']
                    runs = ballEvent[balls]['runs']['batsman']
                    extras = ballEvent[balls]['runs']['extras']
                    total = ballEvent[balls]['runs']['total']
                    try:
                        if ballEvent[balls]['wicket']:
                            wicket = 1
                            kind = ballEvent[balls]['wicket']['kind']
                            playerout = ballEvent[balls]['wicket']['player_out']
                            try:
                                if ballEvent[balls]['wicket']['fielders']:
                                    fielder = ballEvent[balls]['wicket']['fielders'][0]
                            except KeyError:
                                fielder = 'NA'
                    except KeyError:
                        wicket = 0
                        kind = 'NA'
                        fielder = 'NA'
                        playerout = 'NA'

                    try:
                        if ballEvent[balls]['extras']:
                            for type in ballEvent[balls]['extras']:
                                extraskind = type
                    except KeyError:
                        extraskind = 'NA'

                    outfile.write('%s:%s\t%s:%s:%s:%s:%s\t%s:%s:%s:%s:%s:%s:%s\n' % \
                                  (innings + 1, innings_team, balls, runs, extras, extraskind, total, bowler,
                                   batsman,
                                   nonstriker, wicket, kind, playerout, fielder))
