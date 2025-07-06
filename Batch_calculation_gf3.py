from chempy import Substance
import Gravemetric_factor
from Batch_equation_splitting2 import eqtn_split


def batch_calc(moles, compounds, derived, a):
    if (sum(moles) < 99.99 or sum(moles) > 100):
        return []

    else:
        compmasses = []
        for i in range(len(compounds)):
            compmasses.append(Substance.from_formula(compounds[i]).mass * moles[i])

        dermasses = 0
        for i in range(len(derived)):
            if derived[i] == "":
                dermasses = dermasses + Substance.from_formula(compounds[i]).mass * moles[i]
            else:
                dermasses = dermasses + Substance.from_formula(derived[i]).mass * moles[i]

        # compmasses = [compound.molar_mass() * moles[i] for i, compound in enumerate(compounds)]
        total_compmass = sum(compmasses)

        weightfractions = []
        grav_factors = []
        for i in range(len(compmasses)):
            weightfractions.append(
                (compmasses[i] / total_compmass) * a * Gravemetric_factor.grav_factor(compounds[i], derived[i]))
            grav_factors.append(Gravemetric_factor.grav_factor(compounds[i], derived[i]))
        #print(weightfractions)

        # weightfractions = [(mass / total_compmass) * a for mass in compmasses]

        return [weightfractions, dermasses, total_compmass, grav_factors]


'''eq = input("Enter the Equation: ")
batch_wt = int(input("Enter the weight of the batch: "))
data = eqtn_split(eq)
moles = data[0]
compounds = data[1]
derived = data[2]
info = batch_calc(moles, compounds, derived, batch_wt)
wt_frac = info[0]
org_mass = info[1] / 100
der_mass = info[2] / 100
print("The derived mass: ", round(der_mass, 4), "g")
print("The original mass: ", round(org_mass, 4), "g")
print(data[3])'''

"""if __name__ == "__main__":
    moles = [19.8, 15.0, 65.0, 0.1, 0.1]
    compounds = ['Li2CO3', 'ZnO', 'H3BO3', 'Er2O3\xa0', 'Pr2O3']
    print(batch_calc(moles, compounds, ['Li2O', '', 'B2O3', '', ''], 10))"""
