class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, v):
        try:
            if not self.dimension == v.dimension:
                raise ValueError

            new_cordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
            return Vector(new_cordinates)

        except ValueError:
            raise ValueError('Dimesions of vectors must match')

    def __sub__(self, v):
        try:
            if not self.dimension == v.dimension:
                raise ValueError

            new_cordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
            return Vector(new_cordinates)

        except ValueError:
            raise ValueError('Dimesions of vectors must match')

    def __mul__(self, c):
        try:
            if not (type(c) == int or type(c) == float):
                raise ValueError

            new_cordinates = [c * x for x in self.coordinates]
            return Vector(new_cordinates)

        except ValueError:
            raise('Scalar must be of type int or float')
