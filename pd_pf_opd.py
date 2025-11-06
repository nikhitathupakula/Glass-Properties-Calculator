from mendeleev import element
from chempy import Substance
from database import resource_path, load_csv_file
import pandas as pd
from tkinter import simpledialog


def oxy_pack_density(cations, ox_occ, mole_frac, Vm):
    op = []
    for j in range(len(cations)):
        op.append(mole_frac[j] * ox_occ[j])
    OPD = round((1000 * sum(op)) / Vm, 4)
    return op, OPD


def effect_rem(cations, batch_wt, wt_frac, den, compounds, dopant_element=None, dopant_charge=None):
    df = load_csv_file()
    rare_earth_elements = [str(x).strip().lower() for x in df['Rare_Earth_Cat'].values]
    results = []
    identified_rems = []
    z = 0

    # Handle dopant_element type (can be str, list, or None)
    if isinstance(dopant_element, list):
        dopant_element = dopant_element[0] if dopant_element else None
    dopant_element = str(dopant_element).strip().lower() if dopant_element else None

    for c in range(len(cations)):
        cat_clean = str(cations[c]).strip().lower()

        # Match auto-found REMs or user-specified dopant
        if (cat_clean in rare_earth_elements) or (dopant_element and dopant_element == cat_clean):
            identified_rems.append(cations[c])
            z = dopant_charge if dopant_charge else 3  # use given charge or default 3

            mass_rem = wt_frac[c]
            mw_rem = Substance.from_formula(compounds[c]).mass
            conc_rem_ic = (mass_rem * den * 6.0221e23) / (batch_wt * mw_rem)
            conc_rem_ml = round((mass_rem * den * 1000) / (batch_wt * mw_rem), 4)
            ii_dist = (1 / (conc_rem_ic * 10e5)) ** 0.333
            pol_rad = 0.5 * ((3.142 / (6 * conc_rem_ic * 10e5)) ** 0.333)
            pol_rad_cm = 0.5 * ((3.142 / (6 * conc_rem_ic)) ** 0.333)
            field_str = z / (pol_rad_cm ** 2)

            results.append(
                f"Element: {cations[c]}\n"
                f"Concentration (ions/cm³): {conc_rem_ic:.4e}\n"
                f"Concentration (moles/l):  {conc_rem_ml:.4f}\n"
                f"Inter Ionic Radius (m):   {ii_dist:.4e}\n"
                f"Polaron Radius (m):       {pol_rad:.4e}\n"
                f"Field Strength (cm⁻²):    {field_str:.4e}\n"
            )

    if not identified_rems:
        return 0, ["No dopant elements found."]

    return z, results


def optical_basicity(cations, mole_frac, Vm, r_i, op, compounds):
    df = load_csv_file()
    cat_pol_b = True
    ob_b = True
    cat_pol_sum = 0
    molar_refract = (Vm * ((r_i ** 2) - 1)) / (2.52 * ((r_i ** 2) + 2))
    inter_par = 0
    cat_pol_list = []

    for i, cation in enumerate(cations):
        cation_row = df[df['Cation'] == cation]

        if not cation_row.empty and not pd.isna(cation_row['Cat_Pol'].values[0]):
            cat_pol = cation_row['Cat_Pol'].values[0] * 10e-31
            cat_pol_sum += cat_pol * mole_frac[i]
            cat_pol_list.append(cat_pol)
        else:
            cat_pol_b = False
            break

    if not cat_pol_b:
        opt_bas = 0
        for i, comp in enumerate(compounds):
            comp_row = df[df['Comp'] == comp]

            if not comp_row.empty and not pd.isna(comp_row['OB'].values[0]):
                ob_th = comp_row['OB'].values[0]
                opt_bas += mole_frac[i] * ob_th
                ob_b = True
            else:
                ob_b = False
                break

    if not cat_pol_b and not ob_b:
        cat_pol_list = []
        cat_pol_sum = 0
        for i, cation in enumerate(cations):
            try:
                user_input = simpledialog.askfloat("Cation Polarizability",
                                                   f"Enter the cation polarizability for {cation} (in Å³): ")
                cat_pol_list.append(user_input * 10e-31)
                cat_pol_sum += user_input * mole_frac[i]
            except ValueError:
                cat_pol_list.append(0)

        elec_ox_pol = (molar_refract - cat_pol_sum) / sum(op)
        opt_bas = 1.67 * (1 - (1 / elec_ox_pol))

        for d in range(len(cations)):
            cat_pol_value = cat_pol_list[d]
            inter_par += mole_frac[d] * (
                    (3.921 - elec_ox_pol) / (2 * (cat_pol_value + 3.921) * (cat_pol_value + elec_ox_pol))
            )

    elif cat_pol_b:
        elec_ox_pol = (molar_refract - cat_pol_sum) / sum(op)
        opt_bas = 1.67 * (1 - (1 / elec_ox_pol))

        for d in range(len(cations)):
            cat_pol_value = cat_pol_list[d]
            inter_par += mole_frac[d] * (
                    (3.921 - elec_ox_pol) / (2 * (cat_pol_value + 3.921) * (cat_pol_value + elec_ox_pol))
            )

    elif ob_b and not cat_pol_b:
        elec_ox_pol = 1.67 / (1.67 - opt_bas)
        inter_par = 0

    elec_neg_cal = (opt_bas / 0.75) + 0.25

    results = (
        f"Electronic Oxide Polarizability : \t{round(elec_ox_pol, 4)}\n"
        f"Optical Basicity                : \t{round(opt_bas, 4)}\n"
        f"Electro Negativity              : \t{round(elec_neg_cal, 4)}\n"
        f"Interaction Parameter           : \t{round(inter_par, 4)}\n"
    )
    return results
