from case_base import CaseBase
from helpers import check_consistency


def experiment_authoritative_precedents():
    csvs = [
        "data/mushroom.csv",
        "data/churn.csv",
        "data/admission.csv",
    ]
    m = "pearson"

    for csv in csvs:
        print("\n===========================================")
        print(f"Analysing {csv} using the {m} method.")

        # Construct case base
        CB = CaseBase(csv, verbose=True, method=m, max_size=None)

        # Make it consistent
        print(check_consistency(CB))

        # get percentage_trivial_strategies
        # helpers =

        # get n_best_precedents
