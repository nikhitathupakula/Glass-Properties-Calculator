def M_M_sep(moles, compounds, Vm):
    molefrac_list = []
    m_m_sep_list = []
    for index in range(len(compounds)):
        moles_m = moles[index]
        molefrac = moles_m / 100
        molefrac_list.append(molefrac)
        m_m_sep = (Vm / (2 * (1 - molefrac) * 6.0221e23)) ** 0.333
        m_m_sep_list.append(m_m_sep)
    return molefrac_list, m_m_sep_list


def coord_num_avg(mole_frac, Vm, cn_values):
    if cn_values == None:
        cn_out = f" "
        return cn_out
    else:
        avg_cn = 0
        for c in range(len(cn_values)):
            cn_i = cn_values[c]
            avg_cn += cn_i * mole_frac[c]
        nb = (6.0221e23 * avg_cn) / (Vm * 10e-7)
        cn = (
            f"Avg Coordination No. : \t{round(avg_cn, 4)}\n"
            f"Bonds per unit Vol   : \t{nb:.4e}\n"
        )
        return cn


def molar_volume(wt_air, wt_imm, im_liq, org_mass, den_liq=None):
    den_liqs = {'toluene': 0.866, 'xylene': 0.875}
    im_liq = im_liq.lower()

    if im_liq in den_liqs:
        den_liq = den_liqs[im_liq]
    elif den_liq is None:
        raise ValueError(f"Density of {im_liq} must be provided.")

    den_liq = round((wt_air * den_liq) / (wt_air - wt_imm), 4)
    mol_vol = round(org_mass / den_liq, 4)
    return den_liq, mol_vol
