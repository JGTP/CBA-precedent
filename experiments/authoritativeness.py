from case_base import CaseBase
from precedents import get_precedent_distribution


def experiment(csvs, m, make_consistent):
    for csv in csvs:
        print("\n===========================================")
        print(f"Analysing {csv} using the {m} method.")

        for auth_method in [None, "relative", "absolute", "product", "harmonic"]:
            print(f"Evaluating for auth_method={auth_method}...")
            CB = CaseBase(csv, verb=True, method=m, auth_method=auth_method)
            if make_consistent:
                initial_size = len(CB)
                print(f"Initial size: {initial_size}.")
                CB.take_consistent_subset()
                reduced_size = len(CB)
                print(f"Reduced size: {reduced_size}.")
                print(
                    f"Removed {initial_size - reduced_size} ({100*(initial_size - reduced_size)/initial_size} %)."
                )

            print(f"Precedent distribution: {get_precedent_distribution(CB)}.")
            inds = range(len(CB))
            forcings = CB.get_forcings(inds)
            cons_forcings = CB.remove_inconsistent_forcings(inds, forcings)
            print(f"Inconsistent forcings: {len(forcings) - len(cons_forcings)}.")
