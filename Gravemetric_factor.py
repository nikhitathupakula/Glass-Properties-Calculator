from chempy import balance_stoichiometry, Substance


def grav_factor(compounds, derived):
    prod_bal = ["H2O", "CO2", "O2", ["NH3", "H2O"]]
    reac = None
    prod = None
    if derived == "":
        return 1
    else:
        for j in prod_bal:
            try:
                if isinstance(j, list):
                    reac, prod = balance_stoichiometry([compounds], [derived] + j)
                    # print("isinstance List is executing")
                    break
                else:
                    reac, prod = balance_stoichiometry([compounds], [derived, j])
                    break

            except Exception as e:
                # print("Exception received")
                pass

    # print(reac,prod)
    if reac is not None and prod is not None:
        gf = (reac[compounds] * Substance.from_formula(compounds).mass) / (
                    prod[derived] * Substance.from_formula(derived).mass)
        return gf
    else:
        print("Evaluation of Gravimetric factor failed")
