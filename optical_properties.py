def opt_prop(r_i, z, Vm):
    opt_const = z / (4 * 3.142 * 6.0221e23)
    molar_refract = (((r_i ** 2) - 1) / ((r_i ** 2) + 2)) * Vm
    polarizability = opt_const * molar_refract * 10e-7
    reflec_loss = round((((r_i - 1) / (r_i + 1)) ** 2) * 100, 4)
    trans_coeff = round(2 * r_i / ((r_i ** 2) + 1), 4)
    di_const = round(r_i ** 2, 4)
    opt_di_const = round(di_const - 1, 4)
    materialization = round(1 - (molar_refract / Vm), 4)

    results = (
        f"Molar Refract          :           \t{round(molar_refract, 4)} cm³/mol\n"
        f"Polarizability           :           \t{polarizability:.4e} m³\n"
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
        if oxd[0].isupper() and oxd[1].islower():
            cations.append(oxd[0:2])
            if oxd[2].isdigit():
                cat_occ.append(int(oxd[2]))
            else:
                cat_occ.append(1)
        if oxd[0].isupper() and oxd[1].isdigit():
            cations.append((oxd[0]))
            cat_occ.append(int(oxd[1]))
        if oxd[-1].isdigit():
            ox_occ.append(int(oxd[-1]))
        else:
            ox_occ.append(1)
    return cations, cat_occ, ox_occ
