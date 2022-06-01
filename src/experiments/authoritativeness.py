from case_base import CaseBase
from helpers import get_precedent_distribution


def experiment(csvs, m, make_consistent):
    for csv in csvs:
        print("\n===========================================")
        print(f"Analysing {csv} using the {m} method.")

        for auth_method in [None, "relative", "absolute", "product", "harmonic"]:
            print(f"Evaluating for auth_method={auth_method}...")
            CB = CaseBase(csv, verb=True, method=m)
            initial_size = len(CB)
            print(f"Initial size: {initial_size}.")
            if make_consistent:
                CB.take_consistent_subset()
                reduced_size = len(CB)
                print(f"Reduced size: {reduced_size}.")
                print(
                    f"Removed {initial_size - reduced_size} ({100*(initial_size - reduced_size)/initial_size} %)."
                )

            print(
                f"Precedent distribution: {get_precedent_distribution(CB, auth_method)}."
            )
                