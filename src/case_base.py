import operator

import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from termcolor import colored

from case import Case, Coordinate, Dimension


class CaseBase(list):
    # A class for a case base, in essence it is just a list of cases
    # but it has a custom init and extra functions.
    def __init__(
        self,
        csv,
        categoricals=None,
        replace=False,
        manords={},
        verbose=False,
        method="logreg",
        max_size=None,
    ):
        """
        Inputs.
            csv:
                The file path to the (processed) csv file.
            categoricals:
                A list of the categorical columns in the data. This will
                also determine a variable 'ordinals' of ordinal columns. If
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
            manords:
                Allows the user to provide a dictionary mapping columns
                names to desired orders, thereby overriding the default
                behaviour which assigns order based on the 'method' value.
            verbose:
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

        try:
            df = pd.read_csv(csv)
        except FileNotFoundError:
            print(f"File {csv} not found.")
        self.cases = [c for c in df.columns.values if c != "Label"]
        categoricals, ordinals, D = self.determine_columns(manords, categoricals, df)
        D = self.determine_order(
            manords, categoricals, ordinals, D, df, method, replace, verbose
        )
        self.cases = self.load_cases(D, df, max_size)

    def determine_columns(self, manords, categoricals, df):
        # Identify the categorical and ordinal columns (if this hasn't been done yet)
        # by trying to convert the values of the column to integers.
        if categoricals == None:
            categoricals = []
            ordinals = []
            for c in self.cases:
                try:
                    df[c].apply(int)
                    ordinals += [c]
                except ValueError:
                    categoricals += [c]
        else:
            ordinals = [c for c in self.cases if c not in categoricals]

        # Initialize the dimensions using the manually specified ones.
        D = {d: Dimension(d, manords[d]) for d in manords}

        # Remove the columns that are manually specified.
        categoricals = [c for c in categoricals if c not in manords]
        ordinals = [c for c in ordinals if c not in manords]
        return categoricals, ordinals, D

    def determine_order(
        self, manords, categoricals, ordinals, D, df, method, replace, verbose
    ):
        # Determine the order based on a method that works with a 'coefficient function'.
        if method == "pearson" or "logreg":

            # Compute the coefficient dictionary based on either the pearson or logreg method.
            if method == "pearson":
                coeffs = pd.get_dummies(df.drop(manords, axis=1)).corr()["Label"]
            elif method == "logreg":
                X = pd.get_dummies(
                    df.drop(manords, axis=1).drop("Label", axis=1)
                ).to_numpy()
                dcs = pd.get_dummies(df[self.cases]).columns.values
                y = df["Label"].to_numpy()
                scaler = preprocessing.StandardScaler().fit(X)
                X = scaler.transform(X)
                clf = LogisticRegression(random_state=0).fit(X, y)
                coeffs = dict(zip(dcs, clf.coef_[0]))

            # Determine orders of ordinal features using the coeffs dict.
            D.update(
                {
                    c: Dimension(c, operator.le)
                    if coeffs[c] > 0
                    else Dimension(c, operator.ge)
                    for c in ordinals
                }
            )

            # Log the orders of the ordinal features.
            if verbose:
                print("\nPrinting dimension orders.")
                for c in ordinals:
                    print(
                        f"{colored(c, 'red')}: {colored('Ascending' if coeffs[c] > 0 else 'Descending', 'green')} ({round(coeffs[c], 2)})"
                    )

            # Determine orders of categorical features using the coeffs dict.
            for c in categoricals:
                cvals = df[c].unique()
                scvals = sorted(cvals, key=lambda x: coeffs[f"{c}_{x}"])

                # Log the orders of this feature.
                if verbose:
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
                    D[c] = Dimension(c, operator.le)

                # Otherwise, make the relation on the original categorical values.
                else:
                    hd = {(scvals[i], scvals[i + 1]) for i in range(len(scvals) - 1)}
                    trhd = self.tr_closure(df[c].unique(), hd)
                    D[c] = Dimension(c, trhd)
        return D

    # Recursive definition of the transitive closure.
    def Rplus(self, x, R):
        return R[x] | {z for y in R[x] for z in self.Rplus(y, R)}

    # Takes as input a (finite) Hasse Diagram, where the nodes are given by A and
    # the covering relation by R, and return the reflexive transitive closure of R.
    def tr_closure(self, A, R):
        R = {x: {y for y in A if (x, y) in R} for x in A}
        return {(x, x) for x in A} | {(x, y) for x in A for y in self.Rplus(x, R)}

    def load_cases(self, D, df, max_size):
        # Read the rows into a list of cases.
        cases = [
            Case(index, {d: Coordinate(r[d], D[d]) for d in D}, r["Label"])
            for index, r in df.iterrows()
        ]

        # Reduce the size to the desired number, if set.
        if max_size is not None:
            cases = cases[:max_size]

        # Call the list init function to load the cases into the CB.
        return cases
