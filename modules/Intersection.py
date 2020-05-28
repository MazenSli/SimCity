#
# Intersection.py
#
#


class Intersection:
    #
    # Intersection class
    #

    # constructor
    def __init__(self, name=None):
        self.streets = []
        if name is not None:
            setattr(self, 'name', name)

    def addStreet(self, street, direction):
        if hasattr(self, direction):
            raise Exception('Intersection contains already a street in "{}"'.format(direction))
        else:
            self.streets.append(street)
            setattr(self, direction, street)

    def checkDirection(self, direction):
        if hasattr(self, direction):
            return False
        else:
            return True

    def __len__(self):
        return len(self.streets)

    # string representation for class data
    def __str__(self):
        s = 'Intersection: '

        if hasattr(self, 'name'):
            s += self.name + ', '
        s += 'contains ' + str(self.__len__()) + ' streets ('

        containsName = False
        for st in self.streets:
            if hasattr(st, 'name'):
                s += st.name + ', '
                containsName = True

        if containsName:
            s = s[:-2]

        s += ').'
        return s
