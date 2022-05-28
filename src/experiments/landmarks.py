import pandas as pd
from helpers import (
    get_forcing_relations,
    get_landmarks,
    get_n_removals,
    separate_inconsistent_forcings,
)
from case_base import CaseBase


def experiment_landmark_cases():
    csvs = [
        "../data/compas.csv",
        "../data/mushroom.csv",
        "../data/churn.csv",
        "../data/admission.csv",
        "../data/tort.csv",
        "../data/welfare.csv",
        "../data/corels.csv",
    ]
    m = "logreg"

    for csv in csvs:
        print("\n===========================================")
        print(f"Analysing {csv} using the {m} method.")

        CB = CaseBase(csv, verbose=True, method=m, max_size=300)
        analyze(CB)


def analyze(CB):
    print("\nComputing relevant differences between the cases.")
    inds = range(len(CB))

    F, Fd, Fid = get_forcing_relations(CB, inds)
    Id = separate_inconsistent_forcings(CB, inds, F)
    ls = get_landmarks(CB, inds, Fid)

    # Make a DataFrame for holding the analysis results.
    adf = pd.DataFrame()
    adf["Scores"] = [len(Fd[i]) for i in inds]
    adf["Score (same outcome)"] = [len(Fd[i]) - len(Id[i]) for i in inds]
    adf["Score (diff outcome)"] = [len(Id[i]) for i in inds]
    adf["Consistency"] = [int(len(Id[i]) == 0) for i in inds]
    adf["Label"] = [CB[i].s for i in inds]
    adf["Landmark"] = [i in ls[CB[i].s] for i in inds]

    removals = get_n_removals(inds, Id)

    # Print the results of the analysis.
    print(f"\nNumber of cases: {len(CB)}.")
    print(
        f"Percentage consistent cases: {round(adf['Consistency'].describe()['mean']*100, 1)}%."
    )
    print(f"Removals to obtain consistency: {round(removals/len(CB)*100, 1)}%.")
    print(
        f"Percentage trivial cases: {round(((len(CB) - (len(ls[0]) + len(ls[1]))) / len(CB)) * 100, 1)}%."
    )
    print(f"Number of landmarks: {len(ls[0]) + len(ls[1])}.")
