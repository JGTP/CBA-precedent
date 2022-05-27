from analysis import analyze
from case_base import CaseBase


def main():
    small_sets = False
    csvs = [
        "data/compas.csv",
        "data/mushroom.csv",
        "data/churn.csv",
        "data/admission.csv",
        "data/tort.csv",
        "data/welfare.csv",
        "data/corels.csv",
    ]
    m = "logreg"

    for csv in csvs:
        print("\n===========================================")
        print(f"Analysing {csv} using the {m} method.")

        # Load the case base with correlation orders.
        CB = CaseBase(csv, verbose=True, method=m, size=300 if small_sets else None)

        # Run the analysis.
        analyze(CB)


if __name__ == "__main__":
    main()
