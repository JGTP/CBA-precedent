# Define <=_s and <_s in terms of the <= and < relations.
# These are needed for the case class.
import operator

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from tabulate import tabulate
from termcolor import colored
from tqdm import tqdm

from helpers import tr_closure


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
    def __init__(self, name, F, s):
        self.name = name
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


# A class for a case base, in essence it is just a list of cases
# but it has a custom init and extra functions.
class CaseBase(list):
    def __init__(
        self,
        csv,
        catcs=None,
        replace=False,
        manords={},
        verb=False,
        method="logreg",
        size=-1,
    ):
        """
        Inputs.
            csv:
                The file path to the (processed) csv file.
            catcs:
                A list of the categorical columns in the data. This will
                also determine a variable 'ordcs' of ordinal columns. If
                no value is provided it will automatically be defined
                as those columns of which not all values can be converted to
                integers.
            replace:
                A boolean indicating whether the values in the dataframe
                should be replaced based on their order. For example,
                if a column has possible values 'a', 'b', and 'c', with
                increasing correlation with the 'Label' variable respectively,
                then we can simply replace them with 0, 1, and 2 respectively
                together with the usual less-than-or-equal order. If this
                variable is false then the values are not replaced and instead
                the dimension is defined using a set indicating their order.
            ords:
                Allows the user to provide a dictionary mapping columns
                names to desired orders, thereby overriding the default
                behaviour which assigns order based on the 'method' value.
            verb:
                A boolean specifying whether the function should be verbose.
            method:
                A string indicating the desired method of determining the dimension orders,
                possible values are 'logreg' for logistic regression and 'pearson' for the
                Pearson correlation method.
            size:
                Limits the size to the specified integer, if possible.

        Attributes.
            df: The dataframe holding the csv.
            D: A dictionary mapping names of dimensions to a dimension class object.
        """

        # Read the csv file and create a list holding the column names.
        df = pd.read_csv(csv)
        self.df = df
        cs = [c for c in df.columns.values if c != "Label"]

        # Identify the categorical and ordinal columns (if this hasn't been done yet)
        # by trying to convert the values of the column to integers.
        if catcs == None:
            catcs = []
            ordcs = []
            for c in cs:
                try:
                    df[c].apply(int)
                    ordcs += [c]
                except ValueError:
                    catcs += [c]
        else:
            ordcs = [c for c in cs if c not in catcs]

        # Initialize the dimensions using the manually specified ones.
        self.D = {d: Dimension(d, manords[d]) for d in manords}

        # Remove the columns that are manually specified.
        catcs = [c for c in catcs if c not in manords]
        ordcs = [c for c in ordcs if c not in manords]

        # Determine the order based on a method that works with a 'coefficient function'.
        if method == "pearson" or "logreg":

            # Compute the coefficient dictionary based on either the pearson or logreg method.
            if method == "pearson":
                coeffs = pd.get_dummies(df.drop(manords, axis=1)).corr()["Label"]
            elif method == "logreg":
                X = pd.get_dummies(
                    df.drop(manords, axis=1).drop("Label", axis=1)
                ).to_numpy()
                dcs = pd.get_dummies(df[cs]).columns.values
                y = df["Label"].to_numpy()
                scaler = preprocessing.StandardScaler().fit(X)
                X = scaler.transform(X)
                clf = LogisticRegression(random_state=0).fit(X, y)
                coeffs = dict(zip(dcs, clf.coef_[0]))

            # Determine orders of ordinal features using the coeffs dict.
            self.D.update(
                {
                    c: Dimension(c, operator.le)
                    if coeffs[c] > 0
                    else Dimension(c, operator.ge)
                    for c in ordcs
                }
            )

            # Log the orders of the ordinal features.
            if verb:
                print("\nPrinting dimension orders.")
                for c in ordcs:
                    print(
                        f"{colored(c, 'red')}: {colored('Ascending' if coeffs[c] > 0 else 'Descending', 'green')} ({round(coeffs[c], 2)})"
                    )

            # Determine orders of categorical features using the coeffs dict.
            for c in catcs:
                cvals = df[c].unique()
                scvals = sorted(cvals, key=lambda x: coeffs[f"{c}_{x}"])

                # Log the orders of this feature.
                if verb:
                    print(
                        f"{colored(c, 'red')}: "
                        + " < ".join(
                            [
                                f"{colored(v, 'green')} ({round(coeffs[f'{c}_{v}'], 4)})"
                                for v in scvals
                            ]
                        )
                    )

                # Replace the values of the categorical feature with numbers, so that
                # we can simply compare using <= on the naturals, if enabled.
                if replace:
                    for i, val in enumerate(scvals):
                        df[c] = df[c].replace(val, i)
                    self.D[c] = Dimension(c, operator.le)

                # Otherwise, make the relation on the original categorical values.
                else:
                    hd = {(scvals[i], scvals[i + 1]) for i in range(len(scvals) - 1)}
                    trhd = tr_closure(df[c].unique(), hd)
                    self.D[c] = Dimension(c, trhd)

        # Read the rows into a list of cases.
        cases = [
            Case(i, {d: Coordinate(r[d], self.D[d]) for d in self.D}, r["Label"])
            for i, r in df.iterrows()
        ]

        # Reduce the size to the desired number, if set.
        if size != -1:
            cases = cases[:size]

        # Call the list init function to load the cases into the CB.
        super(CaseBase, self).__init__(cases)

    # A function which pretty prints a comparison between cases a and b.
    def compare(self, a, b):
        # Compare two values v,w according to their dimensions order and return the result.
        def R(v, w):
            if v == w:
                return "="
            if v < w:
                return "<"
            elif w < v:
                return ">"
            else:
                return "|"

        # Form a pandas dataframe holding the comparison data.
        compdf = pd.DataFrame(
            {
                "a": [a[d] for d in self.D] + [a.s],
                "R": [R(a[d], b[d]) for d in self.D] + [""],
                "b": [b[d] for d in self.D] + [b.s],
                "F": ["X" if d in a.diff(b) else "" for d in self.D] + [""],
            },
            index=list(self.D.keys()) + ["Label"],
        )

        # Pretty print this dataframe using the tabulate package.
        print(
            tabulate(
                compdf,
                showindex=True,
                headers=["Dimension"] + list(compdf.columns),
                colalign=("left", "right", "center", "left", "center"),
            )
        )

    def take_consistent_subset(self):
        inds = range(len(self))
        forcings = self.get_forcings(inds)
        Id = self.remove_inconsistent_forcings(inds, forcings)
        inconsistent_indices = self.determine_inconsistencies(inds, Id)
        consistent_subset = self.remove_inconsistencies(inconsistent_indices)
        super(CaseBase, self).__init__(consistent_subset)

    def determine_inconsistencies(self, inds, Id):
        to_remove = []
        while sum(s := [len(Id[i]) for i in inds]) != 0:
            k = np.argmax(s)
            for i in inds:
                Id[i] -= {k}
            Id[k] = set()
            to_remove.append(k)
        return to_remove

    def remove_inconsistencies(self, indices):
        consistent_subset = [case for case in self if case.name not in indices]
        return consistent_subset

    def get_forcings(self, inds):
        return {
            (i, j) for i in tqdm(inds, miniters=100) for j in inds if self[i] <= self[j]
        }

    def get_n_trivial_strategies(self, auth_method=None):
        forcings = self.get_forcings(range(len(self)))
        return len(forcings)


    def remove_inconsistent_forcings(self, inds, F):
        # Separate from F the forcings that lead to inconsistency.
        I = {(i, j) for (i, j) in F if self[i].s != self[j].s}
        Id = {i: set() for i in inds}
        for i, j in I:
            Id[i] |= {j}
            Id[j] |= {i}
        return Id