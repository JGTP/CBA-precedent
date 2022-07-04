import pandas as pd
from numpy import full

from experiments import authoritativeness


def generate_row(mean, std, n_inconsistent_forcings, trivial, none, some, all):
    return f"\multicolumn{{1}}{{l|}}{{\\begin{{tabular}}[c]{{@{{}}l@{{}}}}$\mu={mean}$\\\\ $\\sigma={std}$\\\\ $N_{{inc}}={n_inconsistent_forcings}$\\\\ $N_{{tws}}={trivial}$\\\\ $N_{{none}}={none}$\\\\ $N_{{some}}={some}$\\\\ $N_{{all}}={all}$\end{{tabular}}}}"


if __name__ == "__main__":
    exp_dict = {
        "Admission": {
            "path": "data/admission.csv",
            "Full dataset": {
                "auth_methods": {
                    None: {},
                    "relative": {},
                    "absolute": {},
                    "product": {},
                    "harmonic": {},
                },
            },
        },
        "Churn": {
            "path": "data/churn.csv",
            "Full dataset": {
                "auth_methods": {
                    None: {},
                    "relative": {},
                    "absolute": {},
                    "product": {},
                    "harmonic": {},
                },
            },
        },
        # "Mushroom": {
        #     "path": "data/mushroom.csv",
        #     "Full dataset": {
        #         "auth_methods": {
        #             None: {},
        #             "relative": {},
        #             "absolute": {},
        #             "product": {},
        #             "harmonic": {},
        #         },
        #     },
    }
    exp_dict = authoritativeness.experiment(exp_dict)
    for name in exp_dict:
        results = ""
        full_dataset = exp_dict[name].get("Full dataset")
        for auth_method in full_dataset["auth_methods"]:
            mean = full_dataset["auth_methods"][auth_method]["mean"]
            std = full_dataset["auth_methods"][auth_method]["std"]
            n_inconsistent_forcings = full_dataset["auth_methods"][auth_method][
                "Inconsistent forcings"
            ]
            trivial = full_dataset["auth_methods"][auth_method]["trivial"]
            none = full_dataset["auth_methods"][auth_method]["none"]
            some = full_dataset["auth_methods"][auth_method]["some"]
            all = full_dataset["auth_methods"][auth_method]["all"]
            row = generate_row(
                mean, std, n_inconsistent_forcings, trivial, none, some, all
            )
            results += row
            results += "&"
        with open(f"results/{name}.txt", "w") as f:
            print(f"Writing results for {name}.")
            f.write(results)
