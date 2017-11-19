# Public domain. No warranty.

# Compatible: Python 2.7, Python 3.2

"""Vec2d.py - Nice implementation of a 2D vector coordinate.

Source: http://www.pygame.org/wiki/2DVectorClass
"""

import operator
import math

from math import atan2, cos, sin, sqrt, pi, radians
import sys

if sys.version_info[0] == 3:
    from functools import reduce
    xrange = range

import pygame

GEOMETRY_TYPES = RECT_TYPE, CIRCLE_TYPE, LINE_TYPE, POLY_TYPE = tuple(range(4))

class Vec2d(object):
    __slots__ = ['x', 'y']
 
    def __init__(self, x_or_pair, y=None):
        if y is None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
 
    def __len__(self):
        return 2
 
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif isinstance(key, slice):
            # Python 3
            return self.x, self.y
        else:
            raise IndexError("Invalid subscript " + str(key) + " to Vec2d")
 
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif isinstance(key, slice):
            # Python 3
            self.x = value[0]
            self.y = value[1]
        else:
            raise IndexError("Invalid subscript " + str(key) + " to Vec2d")
    
    def __getslice__(self, i, j):
        # Deprecated in Python 3 - see __getitem__.
        return [self.x, self.y][i:j]
    
    def __setslice__(self, i, j, seq):
        # Deprecated in Python 3 - see __setitem__.
        me = [self.x, self.y]
        me[i:j] = seq
        self.x, self.y = me
    
    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)
    
    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False
    
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True
 
    def __nonzero__(self):
        # Python 2.7 - see __bool__ for Python 3
        return bool(self.x or self.y)
 
    def __bool__(self):
        # Python 3 - see __nonzero__ for Python 2.7
        return bool(self.x or self.y)
 
    # Generic operator handlers
    def _o2(self, other, f):
        """Any two-operator operation where the left operand is a Vec2d"""
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif hasattr(other, "__getitem__"):
            return Vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other),
                         f(self.y, other))
 
    def _r_o2(self, other, f):
        """Any two-operator operation where the right operand is a Vec2d"""
        if hasattr(other, "__getitem__"):
            return Vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x),
                         f(other, self.y))
 
    def _io(self, other, f):
        """inplace operator"""
        if hasattr(other, "__getitem__"):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self
 
    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__
    
    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self
 
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)

    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if hasattr(other, "__getitem__"):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)

    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif hasattr(other, "__getitem__"):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self
 
    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x * other.x, self.y * other.y)
        if hasattr(other, "__getitem__"):
            return Vec2d(self.x * other[0], self.y * other[1])
        else:
            return Vec2d(self.x * other, self.y * other)
    __rmul__ = __mul__
    
    def __imul__(self, other):
        if isinstance(other, Vec2d):
            self.x *= other.x
            self.y *= other.y
        elif hasattr(other, "__getitem__"):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self
 
    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)

    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)

    def __idiv__(self, other):
        return self._io(other, operator.div)

    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)

    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)

    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)
 
    def __truediv__(self, other):
        return self._o2(other, operator.truediv)

    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)

    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)
 
    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)

    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
 
    def __divmod__(self, other):
        return self._o2(other, operator.divmod)

    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)
 
    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)

    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
 
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)

    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
 
    def __rshift__(self, other):
        return self._o2(other, operator.rshift)

    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
 
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
 
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
 
    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
 
    # Unary operations
    def __neg__(self):
        return Vec2d(operator.neg(self.x), operator.neg(self.y))
 
    def __pos__(self):
        return Vec2d(operator.pos(self.x), operator.pos(self.y))
 
    def __abs__(self):
        return Vec2d(abs(self.x), abs(self.y))
 
    def __invert__(self):
        return Vec2d(-self.x, -self.y)
 
    # vectory functions
    def get_length_sqrd(self): 
        return self.x ** 2 + self.y ** 2
 
    def get_length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __setlength(self, value):
        length = self.get_length()
        self.x *= value / length
        self.y *= value / length
    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")

    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y
 
    def rotated(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        return Vec2d(x, y)
    
    def get_angle(self):
        if self.get_length_sqrd() == 0:
            return 0
        return math.degrees(math.atan2(self.y, self.x))

    def __setangle(self, angle_degrees):
        self.x = self.length
        self.y = 0
        self.rotate(angle_degrees)
    angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")
 
    def get_angle_between(self, other):
        cross = self.x * other[1] - self.y * other[0]
        dot = self.x * other[0] + self.y * other[1]
        return math.degrees(math.atan2(cross, dot))
            
    def normalized(self):
        length = self.length
        if length != 0:
            return self / length
        return Vec2d(self)
 
    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length
 
    def perpendicular(self):
        return Vec2d(-self.y, self.x)
    
    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vec2d(-self.y / length, self.x / length)
        return Vec2d(self)
        
    def dot(self, other):
        return float(self.x * other[0] + self.y * other[1])
        
    def get_distance(self, other):
        return math.sqrt((self.x - other[0]) ** 2 + (self.y - other[1]) ** 2)
        
    def get_dist_sqrd(self, other):
        return (self.x - other[0]) ** 2 + (self.y - other[1]) ** 2
        
    def projection(self, other):
        other_length_sqrd = other[0] * other[0] + other[1] * other[1]
        projected_length_times_other_length = self.dot(other)
        return other * (projected_length_times_other_length / other_length_sqrd)
    
    def cross(self, other):
        return self.x * other[1] - self.y * other[0]
    
    def interpolate_to(self, other, range):
        return Vec2d(self.x + (other[0] - self.x) * range, self.y + (other[1] - self.y) * range)
    
    def convert_to_basis(self, x_vector, y_vector):
        return Vec2d(self.dot(x_vector) / x_vector.get_length_sqrd(), self.dot(y_vector) / y_vector.get_length_sqrd())
 
    def __getstate__(self):
        return [self.x, self.y]
        
    def __setstate__(self, dict):
        self.x, self.y = dict

class LineGeometry(object):
    collision_type = LINE_TYPE

    def __init__(self, x1, y1, x2, y2, position=None):
        self._p1 = Vec2d(x1, y1)
        self._p2 = Vec2d(x2, y2)
        self._rect = pygame.Rect(0, 0, 1, 1)
        if position is not None:
            self.position = position

    def _get_rect(self):
        r = self._rect
        r.topleft = self._p1
        r.size = self._p2 - self._p1
        r.normalize()
        return r
    rect = property(_get_rect)

    def getpoints(self):
        return tuple(self._p1), tuple(self._p2)

    def setpoints(self, endpoints):
        if len(endpoints) == 4:
            self._p1[:] = endpoints[0:2]
            self._p2[:] = endpoints[2:4]
        elif len(endpoints) == 2:
            self._p1[:] = endpoints[0]
            self._p2[:] = endpoints[1]
        else:
            raise ValueError('{0}.points: endpoints={1}'.format(self.__class__.__name__, endpoints))
    points = property(getpoints, setpoints)
    
    def getend_points(self):
        return self._p1[:], self._p2[:]
    end_points = property(getend_points)
    

    def getposition(self):

        return self._center

    def setposition(self, val):
        x = val[0]
        y = val[1]
        cx, cy = self._center
        dx = x - cx
        dy = y - cy
        #
        p1 = self._p1
        p1[0] += dx
        p1[1] += dy
        #
        p2 = self._p2
        p2[0] += dx
        p2[1] += dy
    position = property(getposition, setposition)
    
    def _getcenter(self):
        p1 = self._p1
        x1 = p1[0]
        y1 = p1[1]
        #
        p2 = self._p2
        x2 = p2[0]
        y2 = p2[1]
        #
        cx = x1 + (x2 - x1) / 2
        cy = y1 + (y2 - y1) / 2
        return Vec2d(cx, cy)
    _center = property(_getcenter)
    
    def getp1(self):
        return self._p1[:]

    def setp1(self, xorxy, y=None):
        if y is None:
            self._p1[:] = xorxy
        else:
            self._p1[:] = xorxy, y
    p1 = property(getp1, setp1)
    
    def getp2(self):
        return self._p2[:]

    def setp2(self, xorxy, y=None):
        if y is None:
            self._p2[:] = xorxy
        else:
            self._p2[:] = xorxy, y
    p2 = property(getp2, setp2)
    
    def getx1(self):
        return self._p1[0]

    def setx1(self, val):
        self._p1[0] = val
    x1 = property(getx1, setx1)
    
    def gety1(self):
        return self._p1[1]

    def sety1(self, val):
        self._p1[1] = val
    y1 = property(gety1, sety1)
    
    def getx2(self):
        return self._p2[0]

    def setx2(self, val):
        self._p2[0] = val
    x2 = property(getx2, setx2)
    
    def gety2(self):
        return self._p2[1]

    def sety2(self, val):
        self._p2[1] = val
    y2 = property(gety2, sety2)

class RectGeometry(object):
    collision_type = RECT_TYPE
    
    def __init__(self, x, y, width, height, position=None):
        super(RectGeometry, self).__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self._position = Vec2d(0.0, 0.0)
        if position is None:
            self.position = self.rect.center
        else:
            self.position = position

    def getpoints(self):
        r = self.rect
        return r.topleft, r.topright, r.bottomright, r.bottomleft
    points = property(getpoints)
    
    def getposition(self):
        return self._position

    def setposition(self, val):
        p = self._position
        p.x, p.y = val
        self.rect.center = round(p.x), round(p.y)
    position = property(getposition, setposition)

def calcAngles(x1, y1, x2, y2):
	return 360-math.atan2(x1-x2,y1-y2)*180/math.pi

def rect_collide_rect(a, b, rect_pre_tested=False):
    coll = True if rect_pre_tested else None
    if coll is None:
        try:
            coll = a.rect.colliderect(b.rect) == True
        except:
            pass
    return coll

def rect_collide_line(a, b, rect_pre_tested=False):
    if a.collision_type != RECT_TYPE:
        a, b = b, a
    rect = a.rect
    end_points = b.end_points
    collidepoint = rect.collidepoint
    return collidepoint(end_points[0]) or len(line_intersects_rect(end_points, rect)) > 0
           # or collidepoint(end_points[1]) == True

def line_collide_line(a, b, rect_pre_tested=False):
    return line_intersects_line(a.end_points, b.end_points)

def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    diffx = x1 - x2
    diffy = y1 - y2
    return (diffx * diffx + diffy * diffy) ** 0.5

def step_toward_point(p1, p2, distance):
    """Calculate the point at a given distance along the line with end points
    (x1,y1) and (x2,y2).

    This function is about twice as fast as the combination angle_of() and
    point_on_circumference().

    The (x1,y1) argument is the origin.

    The (x2,y2) argument is the destination.

    The distance argument is the size of the step, or speed.
    """
    x1, y1 = p1
    x2, y2 = p2
    line = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    step = line / distance
    new_x = x1 + (x2 - x1) / step
    new_y = y1 + (y2 - y1) / step
    return new_x, new_y

def rect_to_lines(rect):
    """Return a list of end-point pairs assembled from a pygame.Rect's corners.
    """
    tl, tr, br, bl = rect.topleft, rect.topright, rect.bottomright, rect.bottomleft
    return [(tl, tr), (tr, br), (br, bl), (bl, tl)]

def line_intersects_line(line_1, line_2):
    def is_on_segment(xi, yi, xj, yj, xk, yk):
        return (xi <= xk or xj <= xk) and (xk <= xi or xk <= xj) and (yi <= yk or yj <= yk) and (yk <= yi or yk <= yj)
    (Ax, Ay), (Bx, By) = line_1
    (Cx, Cy), (Dx, Dy) = line_2
    # d1 = compute_direction(Cx, Cy, Dx, Dy, Ax, Ay)
    a = (Ax - Cx) * (Dy - Cy)
    b = (Dx - Cx) * (Ay - Cy)
    d1 = -1 if a < b else 1 if a > b else 0
    # d2 = compute_direction(Cx, Cy, Dx, Dy, Bx, By)
    a = (Bx - Cx) * (Dy - Cy)
    b = (Dx - Cx) * (By - Cy)
    d2 = -1 if a < b else 1 if a > b else 0
    # d3 = compute_direction(Ax, Ay, Bx, By, Cx, Cy)
    a = (Cx - Ax) * (By - Ay)
    b = (Bx - Ax) * (Cy - Ay)
    d3 = -1 if a < b else 1 if a > b else 0
    # d4 = compute_direction(Ax, Ay, Bx, By, Dx, Dy)
    a = (Dx - Ax) * (By - Ay)
    b = (Bx - Ax) * (Dy - Ay)
    d4 = -1 if a < b else 1 if a > b else 0
    return (
        ((d2 < 0 < d1 or d1 < 0 < d2) and (d4 < 0 < d3 or d3 < 0 < d4)) or
        (d1 == 0 and is_on_segment(Cx, Cy, Dx, Dy, Ax, Ay)) or
        (d2 == 0 and is_on_segment(Cx, Cy, Dx, Dy, Bx, By)) or
        (d3 == 0 and is_on_segment(Ax, Ay, Bx, By, Cx, Cy)) or
        (d4 == 0 and is_on_segment(Ax, Ay, Bx, By, Dx, Dy))
    )

def lines_intersect_lines(lines1, lines2, fast=True):
    crosses = []
    for line1 in lines1:
        for line2 in lines2:
            if line_intersects_line(line1.end_points, line2):
                crosses.append((line1.end_points, line2))
                if fast:
                    return crosses
    return crosses

def lines_point_of_intersection(line_1, line_2):
    a, b = (x1, y1), (x2, y2) = line_1
    c, d = (x3, y3), (x4, y4) = line_2
    
    # Fail if either line segment is zero-length.
    if a == b or c == d:
        return []

    sx1 = float(x2 - x1)
    sy1 = float(y2 - y1)
    sx2 = float(x4 - x3)
    sy2 = float(y4 - y3)

    # Fail if lines coincide (end points are along the same line).
    s1 = (-sx2 * sy1 + sx1 * sy2)
    t1 = (-sx2 * sy1 + sx1 * sy2)
    if s1 == 0 or t1 == 0:
        return []

    s = (-sy1 * (x1 - x3) + sx1 * (y1 - y3)) / s1
    t = (sx2 * (y1 - y3) - sy2 * (x1 - x3)) / t1

    # if s >= 0 and s <= 1 and t >= 0 and t <= 1:
    if 0 <= s <= 1 and 0 <= t <= 1:
        # Collision detected
        i_x = x1 + (t * sx1)
        i_y = y1 + (t * sy1)
        return [(i_x, i_y)]

    # No collision
    return []

def line_intersects_rect(line, rect, fast=True):
    rect_lines = rect_to_lines(rect)
    return lines_intersect_lines([line] , rect_lines, fast)

