import yaml


TYPES = ['discussion', 'theory', 'exercise', 'break']
WORKSHOP = {
    'Workshop': None,
    'Author': None,
    'Description': None
}


def toTime(integer):
    try:
        hours = integer // 60
        minutes = integer - (hours * 60)
        return '{}:{:02} h'.format(hours, minutes)
    except Exception:
        return '0:00 h'


class WPlan(object):
    def __init__(self, string):
        self.Blocks = []
        self.Workshop = WORKSHOP
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
                block = yaml.load(x)
                block['pos_start'] = position
                block['pos_end'] = position + len(x)
                position = block['pos_end'] + 2
            except Exception:
                continue
            if 'Title' in block:
                self.Blocks.append(block)
            elif 'Workshop' in block:
                self.Workshop = block

    def getDurationStr(self, index):
        try:
            return toTime(self.Blocks[index]['Length'])
        except Exception as e:
            print(e)
            return toTime(0)

    def getTimeSum(self):
        time = 0
        for x in self.Blocks:
            try:
                time += int(x['Length'])
            except Exception:
                pass
        return toTime(time)

    def getActualIndex(self, cursor_pos):
        block_index = -1
        for i, x in enumerate(self.Blocks):
            if cursor_pos >= x['pos_start'] and cursor_pos <= x['pos_end']:
                block_index = i
        return block_index

    def getActualTime(self, index):
        start = 0
        for x in self.Blocks[:index]:
            try:
                start += int(x['Length'])
            except Exception:
                pass
        try:
            end = start + int(self.Blocks[index]['Length'])
        except Exception:
            end = start

        return start, end

    def getActualTimeStr(self, index):
        start, end = self.getActualTime(index)
        return '{} - {}'.format(
            toTime(start),
            toTime(end)
        )

    def getMaterials(self):
        materials = {}
        for x in self.Blocks:
            try:
                for m in x['Material']:
                    if m not in materials:
                        materials[m] = [x['Title']]
                    else:
                        materials[m].append(x['Title'])
            except Exception:
                pass
        return materials
