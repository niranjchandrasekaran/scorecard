#Scorecard

Scorecard generates cricket scorecards. It reads a yaml file from [Cricsheet](www.google.com) and generates a scorecard akin to the [cricinfo](http://www.espncricinfo.com/).The code works for IPL scorecards but could possibly work for other T20 or Limited Overs cricket scorecards.

The code is written in python and requires <i>numpy</i>, <i>pandas</i>, <i>more_itertools</i> and <i>yaml</i> packages.

The program accepts either a single yaml file or a text file with a list of yaml files using the <i>-f</i> flag. It then outputs the scorecard as a text file with the extension .scard.