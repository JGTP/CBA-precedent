from tabulate import tabulate


# Define <=_s and <_s in terms of the <= and < relations.
# These are needed for the case class.
def le(s, v1, v2):
    return v1 <= v2 if s == 1 else v1 >= v2


def lt(s, v1, v2):
    return v1 < v2 if s == 1 else v1 > v2


# A dimension is a partially ordered set.
# This order must be specified at creation by the 'le' function.
# Its elements are assumed to be partially ordered by <=, specified
# by the 'le' function, where the default direction is for the plaintiff.
class Dimension:
    def __init__(self, name, le):
        self.name = name
        self.le = le if type(le) != set else lambda x, y: (x, y) in le

    def __eq__(self, d):
        return self.name == d.name and self.le == d.le

    def __repr__(self):
        return f"dim({self.name})"


# A coordonate is a value in some dimension.
# They can be compared using the partial order of the dimension they belong to.
class Coordinate:
    def __init__(self, value, dim):
        self.dim = dim
        self.value = value

    def __le__(self, c2):
        return self.dim.le(self.value, c2.value)

    def __lt__(self, c2):
        return self != c2 and self.dim.le(self.value, c2.value)

    def __ge__(self, c2):
        return self.dim.le(c2.value, self.value)

    def __gt__(self, c2):
        return self != c2 and self.dim.le(c2.value, self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, value):
        return self.value == value


# A class for cases, i.e. fact situations together with an outcome.
# A fact situation is represented as a dictionary mapping the dimensions to
# a coordonate in that dimension.
class Case:
    def __init__(self, F, s):
        self.F = F
        self.s = s

    def __le__(self, d):
        return not any(self.diff(d.F))

    def __getitem__(self, key):
        return self.F[key]

    def __setitem__(self, key, value):
        self.F[key] = value

    def __eq__(self, c):
        return self.F == c.F and self.s == c.s

    def __str__(self):
        table = tabulate(
            [[d, self[d]] for d in self.F],
            showindex=False,
            headers=["d", "c[d]"],
            colalign=("left", "left"),
        )
        sep = len(table.split("\n")[1]) * "-"
        return (
            sep + "\n" + table + "\n" + sep + "\n" + f"Outcome: {self.s}" + "\n" + sep
        )

    def diff(self, G):
        for d in self.F:
            if not le(self.s, self[d], G[d]):
                yield d
