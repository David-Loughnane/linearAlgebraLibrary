from math import sqrt, acos, degrees, pi, sin
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalise the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = ''
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = ''

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
            if type(c) not in (int, float, Decimal):
                raise ValueError

            new_cordinates = [x * Decimal(c) for x in self.coordinates]
            return Vector(new_cordinates)

        except ValueError:
            raise('Scalar must be of type int or float')

    def __truediv__(self, c):
        """Scalar division."""
        try:
            if type(c) not in (int, float, Decimal):
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

    def component_parallel_to(self, v):
        try:
            u = v.normalise()
            weight = self.dot(u)
            return u * weight
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self, v):
        try:
            projection = self.component_parallel_to(v)
            return self - projection
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def area_triangle_with(self, v):
        height = self.component_orthogonal_to(v).magnitude()
        return 0.5 * v.magnitude() * height

    def area_parallelogram_with(self, v):
        height = self.component_orthogonal_to(v).magnitude()
        return v.magnitude() * height

    def cross_product_magnitude(self, v):
        return self.magnitude() * v.magnitude() * sin(self.angle_with(v))

    def cross_product(self, v):
        x1, y1, z1 = self.coordinates
        x2, y2, z2 = v.coordinates

        x = (y1 * z2) - (y2 * z1)
        y = -((x1 * z2) - (x2 * z1))
        z = (x1 * y2) - (x2 * y1)

        return Vector([x, y, z])
