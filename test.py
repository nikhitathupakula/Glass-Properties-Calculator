from optical_properties import opt_prop, comp_split
from Batch_equation_splitting2 import eqtn_split
from Batch_calculation_gf3 import batch_calc
from mmsep_den_cn import M_M_sep, molar_volume, coord_num_avg
from pd_pf_opd import pack_factor, effect_rem, optical_basicity
from density_v2 import molar_volume

eq = input("Enter the Equation: ")
batch_wt = int(input("Enter the weight of the batch: "))
density = float(input("Enter the wt in air: "))
info = eqtn_split(eq)
moles, compounds, derived, oxides = info[0], info[1], info[2], info[3]
know = batch_calc(moles, compounds, derived, batch_wt)
weightfractions, dermasses, total_compmass, grav_factors = know[0], know[1], know[2], know[3]
org_mass = dermasses / 100
Vm = molar_volume(org_mass, density)
sep_info = M_M_sep(moles, compounds, Vm)
lists = comp_split(info[3])
cations, cat_occ, ox_occ = lists[0], lists[1], lists[2]
pf_info = pack_factor(cations, cat_occ, ox_occ, sep_info[0], Vm)
cn_values = []
for oxd in oxides:
    cn_value = int(input(f"Enter the CN for{oxd}: "))
    cn_values.append(cn_value)
cn_info = coord_num_avg(sep_info[0], Vm, cn_values)
rem_info = effect_rem(cations, batch_wt, weightfractions, dens, compounds)
r_i = float(input("Enter the RI: "))
ob_info = optical_basicity(cations, sep_info[0], Vm, r_i, pf_info[1], info[3])
results = opt_prop(r_i, Vm, )
print(Vm, ob_info, results)
