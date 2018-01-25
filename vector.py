from math import sqrt, acos, degrees, pi
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalise the zero vector'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
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
        """Scalar multiplication."""
        try:
            if not (type(c) == int or type(c) == float):
                raise ValueError

            new_cordinates = [x * Decimal(c) for x in self.coordinates]
            return Vector(new_cordinates)

        except ValueError:
            raise('Scalar must be of type int or float')

    def __truediv__(self, c):
        """Scalar division."""
        try:
            if not (type(c) == int or type(c) == float):
                raise ValueError

            new_cordinates = [x / Decimal(c) for x in self.coordinates]
            return Vector(new_cordinates)

        except ValueError:
            raise('Scalar must be of type int or float')

    def magnitude(self):
        """Return the magnitude (Euclidean distance from origin) of a vector using the Pythagorean Theorem."""
        squared_deltas = [x ** 2 for x in self.coordinates]
        return sqrt(sum(squared_deltas))

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def normalise(self):
        """Return normalised (magnitude 1) version of vector."""
        return self / self.magnitude()

    def dot(self, v, tolerance=1e-10):
        dot_product = sum([x * y for x, y in zip(self.coordinates, v.coordinates)])
        if (abs(dot_product) - 1) < tolerance:
            if dot_product > 0:
                return 1.0
            else:
                return -1.0
        else:
            return dot_product

    def angle_with(self, v, in_degrees=False):
        try:
            v1 = self.normalise()
            v2 = v.normalise()

            angle = acos(v1.dot(v2))

            if in_degrees is False:
                return angle
            else:
                return degrees(angle)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Can\'t compute an anlge with the zero vector')
            else:
                raise e

    def is_parallel_to(self, v, tolerance=1e-10):
        if self.is_zero() or v.is_zero():
            return True
        elif self.angle_with(v) == pi or self.angle_with(v) == 0:
            return True
        else:
            return False

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance
