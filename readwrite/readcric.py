import pandas as pd


class ReadCric(object):

    def __init__(self, filename):
        cricfile = open(filename, 'r')
        self.info = []
        self.event = []
        found = False

        for row in cricfile:
            if not found:
                if not row.startswith('#'):
                    self.info.append(row.rstrip())
                else:
                    self.header = [element[1:] if element.startswith('#') else element for element in
                                   row.rstrip().split('\t')]
                    found = True
            else:
                self.event.append(row.rstrip().split('\t'))


class ProcessCric(object):

    def __init__(self):
        pass

    def process_info(self, info):
        return pd.Series([info[row].split(':')[1] for row in range(len(info))], index=[info[row].split(':')[0]
                                                                                       for row in range(len(info))])

    def process_event(self, header, event):
        mergedheader = self.cric_linearize([header[element].split(':') for element in range(len(header))])
        mergedevent = [[] for row in range(len(event))]

        for row in range(len(event)):
            mergedevent[row] = self.cric_linearize([event[row][element].split(':') for element in
                                                    range(len(event[row]))])

        return pd.DataFrame(mergedevent, columns=mergedheader)

    def cric_linearize(self, array):
        mergedarray = []
        for subarray in array:
            mergedarray += subarray

        return mergedarray
