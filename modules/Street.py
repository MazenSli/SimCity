#
# Street.py
#
#


class Street:
    #
    # Street class
    #

    # constructor
    def __init__(self, length, startIs, endIs, name=None):
        self.length = length
        self.startInter = startIs
        self.endInter = endIs
        if name is not None:
            setattr(self, 'name', name)

    def __len__(self):
        return self.length

    # string representation for class data
    def __str__(self):
        s = 'Street: '
        if hasattr(self, 'name'):
            s += self.name + ', '
        s += 'contains ' + str(self.__len__()) + ' blocks.'
        return s
