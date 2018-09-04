import yaml


TYPES = ['discussion', 'theory', 'exercise', 'break']
WORKSHOP = {
    'Workshop': None,
    'Author': None,
    'Description': None,
    'Time': 0
}


def toTime(integer, absolute=False):
    """Integer is input in minutes."""
    try:
        hours = integer // 60
        minutes = integer - (hours * 60)
        if absolute:
            hours = hours % 24
        return '{}:{:02} h'.format(hours, minutes)
    except Exception:
        return '0:00 h'


class WPlan(object):
    def __init__(self, string):
        self.Blocks = []
        self.Workshop = WORKSHOP
        self.init_time = 0
        self.strToBlocks(string)

    def __delitem__(self, key):
        self.Blocks.__delattr__(key)

    def __getitem__(self, key):
        return self.Blocks.__getattribute__(key)

    def __setitem__(self, key, value):
        self.Blocks.__setattr__(key, value)

    def __iter__(self):
        return iter(self.Blocks)

    def strToBlocks(self, string):
        position = 0
        for x in string.split('\n\n'):
            try:
                data = yaml.load(x)
                data['Position start'] = position
                data['Position end'] = position + len(x)
                position = data['Position end'] + 2
            except Exception:
                continue
            if 'Title' in data:
                self.initBlock(data)
            elif 'Workshop' in data:
                self.initWorkshop(data)
        self.initAllData()

    def initBlock(self, data):
        try:
            data['Length string'] = toTime(data['Length'])
        except Exception:
            pass
        self.Blocks.append(data)

    def initWorkshop(self, data):
        try:
            data['Time string'] = toTime(data['Time'], True)
        except Exception:
            pass
        self.Workshop = WORKSHOP
        self.Workshop.update(data)

    def initAllData(self):
        # init additional workshop variables
        self.Workshop['Materials'] = {}

        # init counter for timings
        time = 0
        start = self.Workshop['Time']

        for i, x in enumerate(self.Blocks):

            # add additional timing informatino of the blocks
            self.Blocks[i]['Start relative'] = time
            self.Blocks[i]['Start relative string'] = toTime(time)
            self.Blocks[i]['Start absolute'] = time + start
            self.Blocks[i]['Start absolute string'] = toTime(time + start, True)
            time += x['Length']
            self.Blocks[i]['End relative'] = time
            self.Blocks[i]['End relative string'] = toTime(time)
            self.Blocks[i]['End absolute'] = time + start
            self.Blocks[i]['End absolute string'] = toTime(time + start, True)

            # add additional material information for the workshop
            try:
                for m in x['Material']:
                    if m not in self.Workshop['Materials']:
                        self.Workshop['Materials'][m] = [x['Title']]
                    else:
                        self.Workshop['Materials'][m].append(x['Title'])
            except Exception:
                pass

        # add additional information about the workshop times
        self.Workshop['Start relative'] = 0
        self.Workshop['Start relative string'] = toTime(0)
        self.Workshop['Start absolute'] = start
        self.Workshop['Start absolute string'] = toTime(start, True)
        self.Workshop['End relative'] = time
        self.Workshop['End relative string'] = toTime(time)
        self.Workshop['End absolute'] = time + start
        self.Workshop['End absolute string'] = toTime(time + start, True)
        self.Workshop['Length'] = time
        self.Workshop['Length string'] = toTime(time)

    def getActualIndex(self, cursor_pos):
        block_index = -1
        for i, x in enumerate(self.Blocks):
            if cursor_pos >= x['Position start'] and cursor_pos <= x['Position end']:
                block_index = i
        return block_index
