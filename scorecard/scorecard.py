import pandas as pd
import numpy as np
from more_itertools import unique_everseen


class InningsScorecard(object):

    def __init__(self, innings):
        self.batsman_df = pd.DataFrame(
            columns=['batsman', 'bowler', 'kind', 'fielder', 'runs', 'balls', 'dots', 'fours', 'sixes',
                     'strikerate', 'fowruns', 'fowballs'])

        self.bowler_df = pd.DataFrame(
            columns=['bowler', 'overs', 'dots', 'runs', 'wickets', 'economy', 'fours', 'sixers', 'wides', 'noballs'])

        list_of_batsman = list(unique_everseen(innings.batsman))
        list_of_bowlers = list(unique_everseen(innings.bowler))

        for batsman in list_of_batsman:
            batsman_event = innings.loc[innings.batsman == batsman]

            runs = np.sum(self.convert_to_array(batsman_event.runs, int, array=True))
            balls = len(batsman_event[batsman_event.extraskind != 'wides'])
            dots = self.run_event(batsman_event, '0')
            dots = len(dots[dots.extraskind != 'wides'])
            fours = len(self.run_event(batsman_event, '4'))
            sixers = len(self.run_event(batsman_event, '6'))

            if balls == 0:
                strike_rate = 0
            else:
                strike_rate = 100 * float(runs) / float(balls)

            if np.sum(self.convert_to_array(batsman_event.wicket, int, array=True)) == 0:
                bowler = 'NA'
                kind = 'NA'
                fielder = 'NA'
                fow_runs = 'NA'
                fow_ball = 'NA'
            else:
                idx = batsman_event.loc[batsman_event.wicket == '1'].index[0]
                fow_runs = np.sum(self.convert_to_array(innings.loc[0:idx, 'total'], int, array=True))
                fow_ball = self.convert_to_array(innings.loc[idx, 'ball'], float, array=True)
                wicket_event = batsman_event[batsman_event.wicket == '1']
                bowler = self.convert_to_array(wicket_event.bowler, str, array=False)
                kind = self.convert_to_array(wicket_event.kind, str, array=False)
                fielder = self.convert_to_array(wicket_event.fielder, str, array=False)

            self.batsman_df.loc[list_of_batsman.index(batsman)] = [batsman, bowler, kind, fielder, runs, balls,
                                                                   dots, fours, sixers, strike_rate, fow_runs, fow_ball]

        total_balls = 0

        for bowler in list_of_bowlers:
            bowler_event = innings.loc[innings.bowler == bowler]
            balls = len(bowler_event)
            wides = len(bowler_event[bowler_event.extraskind == 'wides'])
            no_balls = len(bowler_event[bowler_event.extraskind == 'noballs'])
            balls = balls - wides - no_balls
            total_balls += balls
            overs = int(balls / 6) + (int(balls % 6) / 10.0)

            dots = self.run_event(bowler_event, '0')
            dots = len(dots[dots.extraskind != 'wides'])

            runs = np.sum(self.convert_to_array(
                bowler_event.total[(bowler_event.extraskind != 'legbyes') & (bowler_event.extraskind != 'byes')],
                int, array=True))

            wickets = np.sum(self.convert_to_array(bowler_event.wicket[(bowler_event.wicket == '1')]
                                                   [bowler_event.kind != 'run out'], int, array=True))

            econ = (runs * 6) / balls

            fours = len(self.run_event(bowler_event, '4'))
            sixers = len(self.run_event(bowler_event, '6'))

            self.bowler_df.loc[list_of_bowlers.index(bowler)] = [bowler, overs, dots, runs, wickets, econ, fours,
                                                                 sixers, wides, no_balls]

        team = list(unique_everseen(innings.team))
        runs = np.sum(self.convert_to_array(innings.total, int, array=True))
        wickets = np.sum(self.convert_to_array(innings.wicket, int, array=True))
        overs = int(total_balls / 6) + (int(total_balls % 6) / 10.0)
        byes = np.sum(self.convert_to_array(innings.total[innings.extraskind == 'byes'], int, array=True))
        legbyes = np.sum(self.convert_to_array(innings.total[innings.extraskind == 'legbyes'], int, array=True))
        wides = np.sum(self.convert_to_array(innings.total[innings.extraskind == 'wides'], int, array=True))
        noballs = innings[innings.extraskind == 'noballs'].shape[0]
        extras = byes + legbyes + wides + noballs

        self.team_df = pd.DataFrame({'team': [team], 'runs': [runs], 'wickets': [wickets], 'overs': [overs],
                                     'byes': [byes], 'legbyes': [legbyes], 'wides': [wides], 'noballs': [noballs],
                                     'extras': [extras]})

    def convert_to_array(self, pdlist, datatype, array):
        if array:
            return np.asarray(pdlist).astype(datatype)
        else:
            return (np.asarray(pdlist).astype(datatype))[0]

    def run_event(self, batsman_event, run):
        return batsman_event[batsman_event.runs == run]
