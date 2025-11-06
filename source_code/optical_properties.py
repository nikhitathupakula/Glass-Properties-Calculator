def opt_prop(r_i, z, Vm):
    molar_refract = (((r_i ** 2) - 1) / ((r_i ** 2) + 2)) * Vm
    reflec_loss = round((((r_i - 1) / (r_i + 1)) ** 2) * 100, 4)
    trans_coeff = round(2 * r_i / ((r_i ** 2) + 1), 4)
    di_const = round(r_i ** 2, 4)
    opt_di_const = round(di_const - 1, 4)
    materialization = round(1 - (molar_refract / Vm), 4)

    if z != 0:
        opt_const = z / (4 * 3.142 * 6.0221e23)
        polarizability = opt_const * molar_refract * 10e-7
        pol_line = f"Polarizability           :           \t{polarizability:.4e} m³\n"
    else:
        pol_line = "Polarizability           :           \tSkipped (no dopant)\n"

    results = (
        f"Molar Refract          :           \t{round(molar_refract, 4)} cm³/mol\n"
        f"{pol_line}"
        f"Reflection Loss        :           \t{reflec_loss} %\n"
        f"Transmission Coeff.  :           \t{trans_coeff}\n"
        f"Dielectric Const.      :           \t{di_const}\n"
        f"Opt Dielect Const.    :           \t{opt_di_const}\n"
        f"Materialization        :           \t{materialization}"
    )
    return results


def comp_split(oxds):
    cations = []
    cat_occ = []
    ox_occ = []

    for oxd in oxds:
        # --- Detect cation part ---
        if len(oxd) >= 2 and oxd[0].isupper() and oxd[1].islower():
            # Two-letter cation (e.g., Bi, Li, Sr)
            cation = oxd[0:2]
            rest = oxd[2:]
        else:
            # Single-letter cation (e.g., B, W, Y)
            cation = oxd[0]
            rest = oxd[1:]

        # --- Detect cation subscript ---
        cat_num = ""
        for ch in rest:
            if ch.isdigit():
                cat_num += ch
            else:
                break
        cat_occ.append(int(cat_num) if cat_num else 1)
        cations.append(cation)

        # --- Detect oxygen subscript ---
        ox_num = ""
        for ch in reversed(oxd):
            if ch.isdigit():
                ox_num = ch + ox_num
            else:
                break
        ox_occ.append(int(ox_num) if ox_num else 1)

    return cations, cat_occ, ox_occ
