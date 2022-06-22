from experiments import authoritativeness, landmarks

if __name__ == "__main__":
    landmarks.experiment()
    # authoritativeness.experiment(
    #     csvs=[
    #         "data/mushroom.csv",
    #         "data/churn.csv",
    #         "data/admission.csv",
    #     ],
    #     m="pearson",
    #     make_consistent=True,
    # )
    # authoritativeness.experiment(
    #     csvs=[
    #         # "data/mushroom500.csv",
    #         # "data/churn500.csv",
    #         "data/admission.csv",
    #     ],
    #     m="pearson",
    #     make_consistent=False,
    # )
