class Input(object):

    def __init__(self):
        pass

    def file_list(self, args):
        if args.f[-5:] == '.yaml':
            flist = [args.f]
        else:
            with open(args.f, 'r') as fopen:
                flist = [line.rstrip() for line in fopen]

        return flist


class PrintScorecard(object):
    def __init__(self, first_innings, second_innings, filename):
        out_filename = str(filename)[:-4] + 'scard'
        fout = open(out_filename, 'w')

        if first_innings.batsman_df.shape[0] > 0:
            fout.write('1st Innings - %s\n\n' % first_innings.team_df.team[0][0])

            self.print_batting(first_innings.batsman_df, fout)

            self.print_team(first_innings.team_df, fout)

            self.print_bowling(first_innings.bowler_df, fout)

        if second_innings.batsman_df.shape[0] > 0:
            fout.write('2nd Innings - %s\n\n' % second_innings.team_df.team[0][0])

            self.print_batting(second_innings.batsman_df, fout)

            self.print_team(second_innings.team_df, fout)

            self.print_bowling(second_innings.bowler_df, fout)

    def print_batting(self, batsman_df, file_object):
        nbatsman = batsman_df.shape[0]

        file_object.write(
            'Batsman                                                                     R     B    Dots  4s    6s   SR       FOW\n')

        for batsman in range(nbatsman):
            current_batsman = batsman_df.loc[batsman]
            file_object.write('%-30s ' % current_batsman.batsman)

            if current_batsman.bowler == 'NA':
                file_object.write('%-40s ' % str('not out'))
            else:
                if current_batsman.kind == 'run out':
                    file_object.write('%-40s ' % str('run out (' + current_batsman.fielder + ')'))
                elif current_batsman.kind == 'stumped':
                    file_object.write('%-40s ' % str('b ' + current_batsman.bowler + ' st ' + current_batsman.fielder))
                elif current_batsman.kind == 'bowled':
                    file_object.write('%-40s ' % str('b ' + current_batsman.bowler))
                elif current_batsman.kind == 'lbw':
                    file_object.write('%-40s ' % str('lbw b ' + current_batsman.bowler))
                elif current_batsman.kind == 'caught':
                    file_object.write('%-40s ' % str('c ' + current_batsman.fielder + ' b ' + current_batsman.bowler))
                elif current_batsman.kind == 'caught and bowled':
                    file_object.write('%-40s ' % str('c&b ' + current_batsman.bowler))

            file_object.write('%5d ' % int(str(current_batsman.runs)))
            file_object.write('%5d ' % int(str(current_batsman.balls)))
            file_object.write('%5d ' % int(str(current_batsman.dots)))
            file_object.write('%5d ' % int(str(current_batsman.fours)))
            file_object.write('%5d ' % int(str(current_batsman.sixes)))
            file_object.write('%6.2f ' % float(str(current_batsman.strikerate)))

            if current_batsman.fowruns == 'NA':
                file_object.write('\n')
            else:
                file_object.write(
                    '%10s \n' % str(str(current_batsman.fowruns) + '(' + str(current_batsman.fowballs) + ')'))

    def print_bowling(self, bowler_df, file_object):
        nbowler = bowler_df.shape[0]

        file_object.write('Bowler                           O     Dots   R     W  Econ    4s    6s    WD    NB\n')

        for bowler in range(nbowler):
            current_bowler = bowler_df.loc[bowler]
            file_object.write('%-30s ' % current_bowler.bowler)
            file_object.write('%4.1f ' % float(current_bowler.overs))
            file_object.write('%5d ' % int(current_bowler.dots))
            file_object.write('%5d ' % int(current_bowler.runs))
            file_object.write('%5d ' % int(current_bowler.wickets))
            file_object.write('%5.2f ' % float(current_bowler.economy))
            file_object.write('%5d ' % int(current_bowler.fours))
            file_object.write('%5d ' % int(current_bowler.sixers))
            file_object.write('%5d ' % int(current_bowler.wides))
            file_object.write('%5d \n' % int(current_bowler.noballs))

        file_object.write('\n\n')

    def print_team(self, team_df, file_object):
        to_print = str(team_df.runs[0]) + '/' + str(team_df.wickets[0]) + '(' + str(team_df.overs[0]) + ')'
        extras_total = str(team_df.extras[0])
        extras = 'b ' + str(team_df.byes[0]) + ', lb ' + str(team_df.legbyes[0]) + ', w ' \
                 + str(team_df.wides[0]) + ', nb ' + str(team_df.noballs[0])
        file_object.write('Total %s Extras %s(%s)\n\n' % (to_print, extras_total, extras))
